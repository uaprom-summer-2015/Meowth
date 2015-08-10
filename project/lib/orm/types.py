from sqlalchemy.types import SmallInteger, TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
import uuid


class TypeEnum(TypeDecorator):

    impl = SmallInteger

    def __init__(self, enum, *args, **kwargs):
        self._enum = enum
        TypeDecorator.__init__(self, *args, **kwargs)

    def process_bind_param(self, enum, dialect):
        if isinstance(enum, Enum):
            return enum.value
        elif isinstance(enum, int):
            try:
                self._enum(enum)
            except ValueError as e:
                raise TypeError(
                    'cannot use value {} with enum \'{}\''
                    .format(enum, self._enum.__name__)
                ) from e
            else:
                return enum
        return None

    def process_literal_param(self, value, dialect):
        return self._enum(value)

    def process_result_value(self, value, dialect):
        return self._enum(value)


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)
