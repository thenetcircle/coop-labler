from labler.api import IImager
from PIL import Image
from PIL import ImageFile
import base64
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Imager(IImager):
    def __init__(self, env):
        self.env = env

    def load_b64_and_dims(self, file_path, file_name) -> (str, int, int):
        full_path = os.path.join(file_path, file_name)
        with open(os.path.join(full_path), 'rb') as image_file:
            b64_bytes = base64.b64encode(image_file.read())

        im = Image.open(full_path)
        width, height = im.size

        return str(b64_bytes, 'utf-8'), width, height
