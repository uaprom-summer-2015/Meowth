from enum import IntEnum
from sqlalchemy.types import SmallInteger, TypeDecorator


class Role(IntEnum):
    staff = 0
    superuser = 1


class TypeEnum(TypeDecorator):

    impl = SmallInteger

    def process_bind_param(self, value, dialect):
        return Role[value].value

    def process_result_value(self, value, dialect):
        return Role(value).name
