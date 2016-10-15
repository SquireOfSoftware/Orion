from singleton import Singleton

@Singleton
class resource_locator(object):
    def __init__(self):
        resource_locator.resources = {}

    def add(self, name, resource):
        resource_locator.resources[name] = resource

class resource(object):
    def __init__(self, resource_locator):
        #Add class instance to name
        resource_locator.add(self.__class__.__name__, self);