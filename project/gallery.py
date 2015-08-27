import os

from werkzeug.datastructures import FileStorage
from project.models import UploadedImage
from PIL import Image
from PIL.ExifTags import TAGS


IM_EXTENSIONS = frozenset(['.jpg', '.jpeg', '.gif', '.png'])


def remove_exif_orientation(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.jpg' or ext == '.jpeg':
        img = Image.open(file_path)
        exif = img._getexif()
        orientation = 1
        for (k, v) in exif.items():
            if TAGS.get(k) == 'Orientation':
                orientation = v
        if orientation is 6:
            img = img.rotate(-90)
        elif orientation is 8:
            img = img.rotate(90)
        elif orientation is 3:
            img = img.rotate(180)
        elif orientation is 2:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation is 5:
            img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation is 7:
            img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation is 4:
            img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        img.save(file_path)


def upload_file(file_path):
    remove_exif_orientation(file_path)
    with open(file_path, 'rb') as fp:
        file = FileStorage(fp)
        UploadedImage.bl.save_image(
            image=file,
            img_category=UploadedImage.IMG_CATEGORY.gallery,
            do_sync=True,
        )


def images(subdir):
    for i in os.listdir(subdir):
        _, extension = os.path.splitext(i)
        if extension.lower() in IM_EXTENSIONS:
            yield os.path.join(subdir, i)


def load_images(subdir=None):
    if not subdir:
        for _ in range(64):
            upload_file('testdata/images/face-2.jpg')
    else:
        for fp in images(subdir):
            upload_file(fp)
