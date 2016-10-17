from django.db import models

# models.py is what the front end will talk to


class MissionModel(models.Model):
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    creation_time = models.DateTimeField()
    altitude = models.FloatField()
    mission_status_id = models.ForeignKey(MissionStatusModel)


class MissionStatusModel(models.Model):
    name = models.CharField()


class PointOfInterestModel(models.Model):
    x = models.FloatField()
    y = models.FloatField()


class ImageModel(models.Model):
    timestamp = models.DateTimeField()
    filepath = models.CharField()
    mission_id = models.ForeignKey(MissionModel)


class WaypointModel(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    time_arrived = models.DateTimeField()
    mission_id = models.ForeignKey(MissionModel)


class ObstacleModel(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    mission_id = models.ForeignKey(MissionModel)


class DroneModel(models.Model):
    name = models.CharField()
    ip = models.CharField()
    drone_status_id = models.ForeignKey(DroneStatusModel)


class DroneStatusModel(models.Model):
    status_name = models.CharField()


class MetaDataModel(models.Model):
    # blob is a binary large OBject
    data_blob = models.BinaryField()
    timestamp = models.DateTimeField()
    drone_id = models.ForeignKey(DroneModel)