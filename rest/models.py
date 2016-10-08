from django.db import models
from services import singleton
from services import drone_control
from services import drone_metadata

# Create your models here
@Singleton
class ResourceLocator:
    def __init__(self):
        self.control
        self.metadata
        self.dal
        self.mission
        return