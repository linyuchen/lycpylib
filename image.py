import os
from PIL import Image


def compress(path, maxsize: int, quality=70, change_size=True):
    """

    :param change_size:
    :param quality:
    :param path:
    :param maxsize: 文件最大字节数，单位b, 1024b=1kb
    :return:
    """
    file_size = os.path.getsize(path)
    print(file_size)
    if file_size > maxsize:
        i = Image.open(path)
        i = i.convert('RGB')
        size = i.size
        if change_size:
            i = i.resize((int(size[0] * 0.95), int(size[1] * 0.95)))
        i.save(path, quality=quality)
        if file_size > maxsize and change_size:
            compress(path, maxsize, quality-10, change_size)
