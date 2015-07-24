from project.lib.media.validators import allowed_file
from flask import request
from wtforms.validators import ValidationError


def allowed_extension(message=None):
    if message is None:
        message = 'Нельзя отправлять такой тип файла'

    # noinspection PyUnusedLocal
    def _allowed_extension(form, file):
        if not allowed_file(request.files[file.name].filename):
            raise ValidationError(message)

    return _allowed_extension
