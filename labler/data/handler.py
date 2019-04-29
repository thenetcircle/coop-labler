import glob
import os
import shutil
import traceback
from multiprocessing.pool import Pool

import numpy as np
from skimage import io
from skimage import transform
from PIL import Image
from PIL import ImageFile
from tqdm import tqdm

from labler.cli import AppSession
from labler.data import IDataHandler
from labler import errors

ImageFile.LOAD_TRUNCATED_IMAGES = True


def _resize(image_file):
    im_parts = image_file.rsplit('.', maxsplit=1)
    rz_file_name = f'{im_parts[0]}_th.{im_parts[1]}'
    image = load_image(image_file)

    # seems for some images skimage (pillow?) returns an array of the image, need to extract it
    if image.shape == (2,):
        image = image[0]

    resized_image = transform.resize(image, output_shape=(500, 500, 3), mode='reflect', anti_aliasing=True)
    io.imsave(rz_file_name, resized_image)

    return rz_file_name


def load_image(image_file):
    """
    Sometimes skimage will hang when loading an image in gpu-02, but not on gpu-01.
    Internally skimage uses PIL to open images, but somewhere it gets stuck. Using
    PIL directly seems to work around the issues, so try that first. The only downsize
    we have to do the conversion to np arrays manually and for some image formats
    this might not work, cause some corner case is not covered, so try to use skimage
    when using PIL fails.
    """
    try:
        image = Image.open(image_file)
        return pillow2array(image)
    except Exception:
        pass

    try:
        return io.imread(image_file)
    except Exception as e:
        raise errors.FatalException(f'PIL/skimage could not open image {image_file}, giving up: {str(e)}')


def pillow2array(img):
    arr = np.array(img.getdata(), np.uint8)
    return arr.reshape((
        img.size[1],
        img.size[0],
        len(img.getbands())  # might be greyscale (1 channel), RGB (3 channels) or transparent (4 channels)
    ))


class DataHandler(IDataHandler):
    EXTENSIONS = {'jpg', 'jpeg', 'png'}

    def __init__(self, env):
        from labler.environ import LablerEnvironment
        self.env: LablerEnvironment = env

    def sync_data_dir(self, project_name: str, app: AppSession, data_dir: str) -> None:
        all_examples = self.env.db.get_examples(project_name)
        examples = [example for example in all_examples if example.file_path.startswith(data_dir)]

        if len(examples) == 0:
            return

        for example in examples:
            full_path = os.path.sep.join([example.file_path, example.file_name])
            if not os.path.exists(full_path):
                if app.lambdaenv.pretend:
                    app.printer.notice(f'example for {full_path} does not exist, would disable')
                else:
                    app.printer.warning(f'example for {full_path} does not exist, disabling')
                    self.env.db.disable_example(example)

    def export_labels(self, project_name: str, app: AppSession, output_dir: str) -> None:
        labels = self.env.db.get_labels(project_name)
        labels_per_name = dict()

        for label in labels:
            bbox = ','.join(map(str, [label.xmin, label.xmax, label.ymin, label.ymax, label.target_class]))
            if label.file_name not in labels_per_name:
                labels_per_name[label.file_name] = bbox
                continue

            existing_bbox = labels_per_name[label.file_name]
            labels_per_name[label.file_name] = f'{existing_bbox} {bbox}'

        for label_name, bboxes in labels_per_name.items():
            label_name = label_name.rsplit('.', maxsplit=1)[0]
            label_name = label_name + '.txt'

            output_file = os.path.join(output_dir, label_name)
            if os.path.exists(output_file):
                if app.lambdaenv.overwrite:
                    os.remove(output_file)
                else:
                    app.printer.warning(f'file {output_file} already exists, skipping (overwrite with --overwrite/-o)')
                    continue

            with open(os.path.join(output_dir, label_name), 'w') as f:
                f.write(f'{label_name} {bboxes}')

    def add_data_dir(self, project_name: str, app: AppSession, data_dir: str) -> None:
        batch = list()
        current_idx = 0
        files = glob.glob(f'{data_dir}/**/*', recursive=True)
        app.printer.blanknotice('')
        to_resize = list()

        for filename in tqdm(files, desc='finding data'):
            if filename is None:
                continue
            if os.path.isdir(filename):
                continue
            if os.path.getsize(filename) == 0:
                continue
            if '.' not in filename:
                continue
            if filename.split('.')[-1].lower() not in DataHandler.EXTENSIONS:
                continue
            if filename.rsplit('.', maxsplit=1)[0].endswith('_th'):
                continue

            try:
                batch.append(self._open_data(filename))
                current_idx += 1
            except Exception as e:
                app.printer.error(f'could not add {filename}: {str(e)}')
                if app.lambdaenv.verbose:
                    print(traceback.format_exc())
                continue

            to_resize.append(filename)

            if current_idx % 100 == 0:
                self.env.db.add_examples(project_name, app, batch)
                batch = list()

        if len(batch) > 0:
            self.env.db.add_examples(project_name, app, batch)

        self.resize(app, to_resize)

        return current_idx

    def resize(self, app: AppSession, to_resize: list):
        with Pool(app.lambdaenv.cores) as p:
            rz_file_names = list(tqdm(p.imap(_resize, to_resize), total=len(to_resize), desc='creating thumbnails'))

        output_dir = app.lambdaenv.output
        if len(rz_file_names) == 0 or output_dir is None:
            return

        for rz_file_name in rz_file_names:
            rz_name = rz_file_name.split(os.path.sep)[-1]
            output_file = os.path.join(output_dir, rz_name)

            if os.path.exists(output_file):
                if not app.lambdaenv.overwrite:
                    app.printer.warning('thumbnail {} exists in output directory {}'.format(rz_name, output_dir))
                    continue
                os.remove(output_file)

            shutil.move(rz_file_name, output_dir)

    def _open_data(self, file_path) -> (str, str, int, int):
        file_name = file_path.split(os.path.sep)[-1]
        base_path = os.path.sep.join(file_path.split(os.path.sep)[:-1])

        with Image.open(file_path) as im:
            width, height = im.size

        return base_path, file_name, int(width), int(height)
