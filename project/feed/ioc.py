class Registry:
    _resources = None

    def __init__(self):
        self._resources = {}

    def put(self, name, func):
        self._resources[name] = func

    def get(self, name):
        return self._resources[name]

    def __getattr__(self, attr_name):
        return self.get(attr_name)


registry = Registry()


class Resource:
    resource_name = None

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def _process_resource_bl(self, instance, resource):
        return resource(instance)

    def __get__(self, instance, clazz):
        if not instance:
            raise AttributeError()

        if self.resource_name not in instance.__dict__:
            resource = registry.get(self.resource_name)

            if self.resource_name.startswith("bl."):
                resource = self._process_resource_bl(instance, resource)
                instance.__dict__[self.resource_name] = resource

        return instance.__dict__[self.resource_name]
