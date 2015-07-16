import weakref
# from project.bl.auth import UserBL
# from project.bl.feed import CategoryBL, VacancyBL, CityBL


class Registry:
    _resources = {}

    def __getitem__(self, name):
        return self._resources[name]

    def __setitem__(self, name, func):
        self._resources[name] = func

    # def __getattr__(self, attr_name):
    #     return self.get(attr_name)


registry = Registry()


class Resource:
    resource_name = None

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def __get__(self, instance, clazz):
        if instance:
            target = instance
        else:
            target = clazz

        if self.resource_name not in target.__dict__:
            func = registry[self.resource_name](target)
            setattr(target, self.resource_name, func)

        return target.__dict__[self.resource_name]


class BaseBL:
    _model = None

    def __init__(self, model):
        self._model = weakref.ref(model)

    @property
    def model(self):
        return self._model()

    def get(self, id_):
        return self.model.query.get(id_)

    def create(self, data):
        vacancy = self.model(**data)
        vacancy.save()
        return vacancy

    def update(self, data):
        model = self.model
        for key, value in data.items():
            setattr(model, key, value)
        model.save()
        return model
