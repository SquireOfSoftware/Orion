

from resource_locator import resource, resource_locator
from database_access_layer import connector

class mission_reader(connector, resource):
    def __init__(self, resource_locator):
        super(resource_locator);

    def read(self):
        connector.connect()