from singleton import Singleton


@Singleton
class resource_locator(object):

    def __init__(self):
        resource_locator.resources = {}

    def add(self, name, resource):
        resource_locator.resources[name] = resource

    def get(self, name):
        return resource_locator.resources[name]


class resource(object):
    def __init__(self, resource_locator):
        # Add class instance to name
        resource_locator.add(self.__class__.__name__, self)
        self.locator = resource_locator
        self.count = 1

    def acquire(self):
        #Lock the resource while there it is not available.
        while (self.count is 0):
            pass
        self.count -= 1

    def release(self):
        self.count += 1

