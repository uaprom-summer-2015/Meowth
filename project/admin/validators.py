from project.lib.media.validators import allowed_image
from flask import request
from wtforms.validators import ValidationError
from PIL import Image


def AllowedExtension(message=None):
    if message is None:
        message = 'Нельзя отправлять такой тип файла'

    # noinspection PyUnusedLocal
    def _allowed_extension(form, file):
        if not allowed_image(request.files[file.name].filename):
            raise ValidationError(message)

    return _allowed_extension


def AllowedMime(message=None):
    if message is None:
        message = 'Нельзя отправлять такой тип файла'

    # noinspection PyUnusedLocal
    def _allowed_mime(form, file):
        # Warning! Crutch ahead!
        try:
            Image.open(request.files[file.name].stream)
            request.files[file.name].stream.seek(0)
        except IOError as ioe:
            raise ValidationError(message) from ioe

    return _allowed_mime
