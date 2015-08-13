from PIL import Image
import io
from project.extensions import celery


@celery.task()
def celery_make_thumbnail(path_to_original, destination, size):
    image = open(path_to_original, 'rb')
    file_bytes = image.read()
    image.close()
    thumb = Image.open(io.BytesIO(file_bytes))
    thumb.thumbnail(size, Image.LANCZOS)
    thumb.save(destination)
