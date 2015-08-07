import Image
from project.extensions import celery


@celery.task()
def celery_make_thumbnail(path_to_original, destination, size):
    thumb = Image.open(path_to_original)
    thumb.thumbnail(size, Image.LANCZOS)
    thumb.save(destination)
