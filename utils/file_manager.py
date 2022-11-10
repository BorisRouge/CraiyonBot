import PIL.Image as Img
import io
import os
import base64


class Images:
    def __init__(self, data: dict, owner: int, prompt: str):
        self.data = data
        self.owner = owner
        self.prompt = prompt
        self.paths: list = []

    def save_images(self):
        path = f'image_storage/' \
               f'user:{self.owner}/{self.prompt[:32]}'

        def make_path(path):
            try:
                os.makedirs(path)
            except FileExistsError:
                path += '_'
                make_path(path)
        make_path(path)

        length = len(self.data['images'])
        for i in range(length):
            bytes_data = base64.b64decode(self.data['images'][i])
            image = Img.open(io.BytesIO(bytes_data))
            image.save(f'{path}/{i}of{length}.png')
            self.paths.append(f'{path}/{i}of{length}.png')
