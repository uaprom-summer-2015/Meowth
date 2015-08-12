from flask import request, current_app
from wtforms.validators import ValidationError
import magic as friendship  # cause friendship is magic


class AllowedMime:

    def __init__(self, mimes=None, message=None):
        self.mimes = mimes
        if not message:
            message = u'Нельзя отправлять такой тип файла'
        self.message = message

    def __call__(self, form, field):
        if self.mimes is None:
            self.mimes = current_app.config['ALLOWED_MIMES']
        # unfortunately it is necessary to read whole file to determine mime
        buf = request.files[field.name].stream.read()
        request.files[field.name].stream.seek(0)
        if not AllowedMime.validate(buf, self.mimes):
            raise ValidationError(self.message)

    @staticmethod
    def validate(buf, mimes):
        mime = friendship.from_buffer(buf, mime=True).decode()
        return mime in mimes
