from PIL import Image, ImageOps
import io
from project.extensions import celery


@celery.task()
def celery_make_thumbnail(path_to_original, destination, size):
    image = open(path_to_original, 'rb')
    file_bytes = image.read()
    image.close()
    thumb = Image.open(io.BytesIO(file_bytes))
    thumb = ImageOps.fit(thumb, size, Image.ANTIALIAS)
    thumb.save(destination)
