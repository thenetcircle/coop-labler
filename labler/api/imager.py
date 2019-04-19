from labler.api import IImager
from PIL import Image
import base64
import os


class Imager(IImager):
    def __init__(self, env):
        self.env = env

    def load_b64(self, file_path, file_name) -> str:
        with open(os.path.join(file_path, file_name), 'rb') as image_file:
            b64_bytes = base64.b64encode(image_file.read())

        im = Image.open('whatever.png')
        width, height = im.size
        return str(b64_bytes, 'utf-8')
