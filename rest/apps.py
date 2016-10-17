from django.apps import AppConfig

class RESTDBConfig(AppConfig):

    name = "rest"
    verbose_name = "REST DB"

    def import_models(self):
        from models import Drone
        from models import Dronestatus