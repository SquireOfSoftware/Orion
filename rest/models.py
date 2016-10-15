from django.db import models
from services import singleton
from services.drone_control import drone_control
from services.drone_metadata import drone_metadata
from services import database_access_layer

# Create your models here
@Singleton
class ResourceLocator:
    def __init__(self):
        self.control = drone_control()
        self.metadata = drone_metadata()
        self.dal = database_layer()
        self.mission =
        return