from wtforms.validators import ValidationError

class Exists(object):
    def __init__(self, model, message=None, reverse=False):
        self.model = model
        self.message = message
        self.reverse = reverse

    def __call__(self, _, field):
        if field.object_data == field.data:
            return
        if not self.message:
            if not self.reverse:
                self.message = 'Запись с таким {} уже существует'\
                    .format(field.name)
            else:
                self.message = 'Запись с таким {} не существует'\
                    .format(field.name)
        q = (self.model
                 .query
                 .filter(getattr(self.model, field.name) == field.data)
             )
        if self.reverse ^ bool(list(q)):
                raise ValidationError(self.message)
