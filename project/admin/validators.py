from flask import request, current_app
from wtforms.validators import ValidationError
import magic as friendship  # cause friendship is magic


class AllowedExtension:
    def __init__(self, extensions=None, message=None):
        self.extensions = extensions
        if not message:
            message = u'Нельзя отправлять файл с таким расширением'
        self.message = message

    def __call__(self, form, field):
        if self.extensions is None:
            self.extensions = current_app.config['ALLOWED_EXTENSIONS']
        filename = request.files[field.name].filename
        AllowedExtension.validate(filename, self.extensions, self.message)

    @staticmethod
    def validate(filename, extensions, message):
        if '.' not in filename:
            raise ValidationError(message)
        name, ext = filename.rsplit('.', 1)
        if ext not in extensions:
            raise ValidationError(message)


class AllowedMime:
    def __init__(self, mimes=None, message=None):
        self.mimes = mimes
        if not message:
            message = u'Нельзя отправлять такой тип файла'
        self.message = message

    def __call__(self, form, field):
        if self.mimes is None:
            self.mimes = current_app.config['ALLOWED_MIMES']
        header = request.files[field.name].stream.read(16)
        request.files[field.name].stream.seek(0)
        AllowedMime.validate(header, self.mimes, self.message)

    @staticmethod
    def validate(header, mimes, message):
        magic = friendship.Magic(mime=True)
        mime = magic.from_buffer(header).decode()
        if mime not in mimes:
            raise ValidationError(message)
