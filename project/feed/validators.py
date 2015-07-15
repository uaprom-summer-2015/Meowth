from project.lib.media.validators import allowed_file
from flask import request
from wtforms.validators import ValidationError
from flask import g


def allowed_extension(message=None):
    if message is None:
        message = 'Нельзя отправлять такой тип файла'

    def _allowed_extension(form, file):
        if not allowed_file(request.files[file.name].filename):
            raise ValidationError(message)

    return _allowed_extension


def max_size(size=None, message=None):
    if size is None:
        size = 15 * 1024 * 1024 + 1
    if message is None:
        message = 'Файл слишком большой.\n \
        Максимальный размер = {} Mib'.format(round(size/1024/1024, 1))

    def _max_size(form, file):
        file = request.files[file.name]
        file_name = file.filename
        file_type = file.content_type
        file_bytes = file.read(size)
        if len(file_bytes) == size:
            raise ValidationError(message)
        else:
            g.file = file_bytes
            g.file_name = file_name
            g.file_type = file_type

    return _max_size
