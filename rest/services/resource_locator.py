from database_access_layer import *

class resource_locator(object):

    def __init__(self):
        resource_locator.resources = {}

    def add(self, name, resource):
        resource_locator.resources[name] = resource

    def get(self, name):
        return resource_locator.resources[name]

    def getDroneControl(self):
        return self.get('drone_control')

    def getDroneMedia(self):
        return self.get('drone_media')

    def getDroneMetadata(self):
        return self.get('drone_metadata')

    def getDroneMission(self):
        return self.get('drone_mission')


class resource(connector):
    def __init__(self, resource_locator):
        # Add class instance to name
        super(resource, self).__init__()
        super(resource, self).connect()
        print "Resource Init"
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

    def connect(self):
        super(resource, self).connect()

    def disconnect(self):
        super(resource, self).disconnect()

    def cursor(self):
        return super(resource, self).cursor()

    def connection(self):
        return super(resource, self).connection()

    def locator(self):
        return self.locator
