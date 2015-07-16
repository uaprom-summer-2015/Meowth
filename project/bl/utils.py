import weakref


class Registry:
    _resources = None

    def __init__(self):
        self._resources = {}
        self._static_resources = {}

    def get(self, name):
        return self._resources[name]

    def put(self, name, func):
        self._resources[name] = func

    def __getattr__(self, attr_name):
        return self.get(attr_name)


registry = Registry()


class Resource:
    resource_name = None

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def _process_resource_bl(self, target, resource):
        return resource(target)

    def __get__(self, instance, clazz):
        if instance:
            target = instance
        else:
            target = clazz

        if self.resource_name not in target.__dict__:
            resource = registry.get(self.resource_name)
            resource = self._process_resource_bl(target, resource)
            setattr(target, self.resource_name, resource)

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

    def all(self):
        return self.model.query.all()

    def update(self, data):
        model = self.model
        for key, value in data.items():
            setattr(model, key, value)
        model.save()
        return model
