from sqlalchemy import true


class ConditionHidden:
    def __get__(self, instance, cls):
            return instance.is_hidden if instance else cls.is_hidden == true()


class ConditionDeleted:
    def __get__(self, instance, cls):
        return instance.is_deleted if instance else cls.is_deleted == true()
