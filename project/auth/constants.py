from sqlalchemy.types import SmallInteger, TypeDecorator

class TypeEnum(TypeDecorator):

    impl = SmallInteger

    def __init__(self, enum, *args, **kwargs):
        self._enum = enum
        TypeDecorator.__init__(self, *args, **kwargs)

    def process_bind_param(self, enum, dialect):
        return enum.value

    def process_result_value(self, value, dialect):
        return self._enum(value)