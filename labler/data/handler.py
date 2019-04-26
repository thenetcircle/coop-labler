import os
import glob
import traceback

from labler.cli import AppSession
from labler.data import IDataHandler

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class DataHandler(IDataHandler):
    EXTENSIONS = {'jpg', 'jpeg', 'png'}

    def __init__(self, env):
        self.env = env

    def add_data_dir(self, project_name: str, app: AppSession, data_dir: str) -> None:
        batch = list()
        current_idx = 0

        for filename in glob.iglob(f'{data_dir}/**/*', recursive=True):
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

            try:
                batch.append(self._open_data(filename))
                current_idx += 1
            except Exception as e:
                app.printer.error(f'could not add {filename}: {str(e)}')
                if app.lambdaenv.verbose:
                    print(traceback.format_exc())
                continue

            if current_idx % 100 == 0:
                self.env.db.add_examples(project_name, app, batch)
                batch = list()

        if len(batch) > 0:
            self.env.db.add_examples(project_name, app, batch)

        return current_idx

    def _open_data(self, file_path) -> (str, str, int, int):
        file_name = file_path.split(os.path.sep)[-1]
        base_path = os.path.sep.join(file_path.split(os.path.sep)[:-1])

        with Image.open(file_path) as im:
            width, height = im.size

        return base_path, file_name, int(width), int(height)