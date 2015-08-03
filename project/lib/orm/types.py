from sqlalchemy.types import SmallInteger, TypeDecorator
from enum import Enum


class TypeEnum(TypeDecorator):

    impl = SmallInteger

    def __init__(self, enum, *args, **kwargs):
        self._enum = enum
        TypeDecorator.__init__(self, *args, **kwargs)

    def process_bind_param(self, enum, dialect):
        if isinstance(enum, Enum):
            return enum.value
        elif isinstance(enum, int):
            if enum not in self._enum.__members__.values():
                raise TypeError(
                    'cannot use value {} with enum \'{}\''
                    .format(enum, self._enum.__name__)
                )
            return enum
        return None

    def process_literal_param(self, value, dialect):
        return self._enum(value)

    def process_result_value(self, value, dialect):
        return self._enum(value)
