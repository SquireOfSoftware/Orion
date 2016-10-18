# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class DroneStatus(models.Model):
    dronestatusid = models.AutoField(db_column='DroneStatusID', primary_key=True)  # Field name made lowercase.
    dronestatusname = models.CharField(db_column='DroneStatusName', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DroneStatus'
        app_label = 'DroneStatus'

    def as_dict(self):
        return {
            "id": self.dronestatusid,
            "status": self.dronestatusname
        }

    # def __str__(self):
    #     return "{}"

class Drone(models.Model):
    droneid = models.IntegerField(db_column='DroneID', primary_key=True)  # Field name made lowercase.
    dronename = models.CharField(db_column='DroneName', max_length=10, blank=True, null=True)  # Field name made lowercase.
    droneip = models.CharField(db_column='DroneIP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    dronestatus_dronestatusid = models.ForeignKey(DroneStatus, models.DO_NOTHING, db_column='DroneStatus_DroneStatusID', null=False)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'Drone'
        app_label = "Drone"

    def as_dict(self):
        return {
            "id": self.droneid,
            "ip": self.droneip,
            "name": self.dronename,
            "status": self.dronestatus_dronestatusid.dronestatusid
        }

    # def __str__(self):
    #     return str(self.droneid)





class Image(models.Model):
    imageid = models.IntegerField(db_column='ImageID')  # Field name made lowercase.
    imagetimestamp = models.DateTimeField(db_column='ImageTimestamp', blank=True, null=True)  # Field name made lowercase.
    imagefilepath = models.CharField(db_column='ImageFilepath', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mission_missionid = models.ForeignKey('Mission', models.DO_NOTHING, db_column='Mission_MissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Image'
        unique_together = (('imageid', 'mission_missionid'),)
        app_label = "Image"


class Metadata(models.Model):
    metadataid = models.IntegerField(db_column='MetadataID')  # Field name made lowercase.
    metadatablob = models.TextField(db_column='MetadataBlob', blank=True, null=True)  # Field name made lowercase.
    metadatatimestamp = models.DateTimeField(db_column='MetadataTimestamp', blank=True, null=True)  # Field name made lowercase.
    drone_droneid = models.ForeignKey(Drone, models.DO_NOTHING, db_column='Drone_DroneID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Metadata'
        unique_together = (('metadataid', 'drone_droneid'),)
        app_label = "Metadata"


class Mission(models.Model):
    missionid = models.IntegerField(db_column='MissionID', primary_key=True)  # Field name made lowercase.
    missionstarttime = models.DateTimeField(db_column='MissionStartTime', blank=True, null=True)  # Field name made lowercase.
    missionendtime = models.DateTimeField(db_column='MissionEndTime', blank=True, null=True)  # Field name made lowercase.
    missioncreationdate = models.DateTimeField(db_column='MissionCreationDate')  # Field name made lowercase.
    missionaltitude = models.FloatField(db_column='MissionAltitude', blank=True, null=True)  # Field name made lowercase.
    missionstatus_missionstatustid = models.ForeignKey('Missionstatus', models.DO_NOTHING, db_column='MissionStatus_MissionStatustID', blank=True, null=True)  # Field name made lowercase.
    drone_droneid = models.ForeignKey(Drone, models.DO_NOTHING, db_column='Drone_DroneID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mission'
        app_label = "Mission"


class Missionstatus(models.Model):
    missionstatustid = models.AutoField(db_column='MissionStatustID', primary_key=True)  # Field name made lowercase.
    missionstatusname = models.CharField(db_column='MissionStatusName', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MissionStatus'
        app_label = "MissionStatus"


class Obstacle(models.Model):
    obstacleid = models.IntegerField(db_column='ObstacleID')  # Field name made lowercase.
    obstaclecoordinatex = models.FloatField(db_column='ObstacleCoordinateX', blank=True, null=True)  # Field name made lowercase.
    obstaclecoordinatey = models.FloatField(db_column='ObstacleCoordinateY', blank=True, null=True)  # Field name made lowercase.
    mission_missionid = models.ForeignKey(Mission, models.DO_NOTHING, db_column='Mission_MissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Obstacle'
        unique_together = (('obstacleid', 'mission_missionid'),)
        app_label = "Obstacle"


class Pointofinterest(models.Model):
    pointofinterestidpointofinterestid = models.IntegerField(db_column='PointOfInterestIDPointOfInterestID')  # Field name made lowercase.
    pointofinterestx = models.FloatField(db_column='PointOfInterestX', blank=True, null=True)  # Field name made lowercase.
    pointofinteresty = models.FloatField(db_column='PointOfInterestY', blank=True, null=True)  # Field name made lowercase.
    mission_missionid = models.ForeignKey(Mission, models.DO_NOTHING, db_column='Mission_MissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PointOfInterest'
        unique_together = (('pointofinterestidpointofinterestid', 'mission_missionid'),)
        app_label = "PointOfInterest"


class Waypoint(models.Model):
    waypointid = models.IntegerField(db_column='WaypointID')  # Field name made lowercase.
    waypointy = models.FloatField(db_column='WaypointY', blank=True, null=True)  # Field name made lowercase.
    waypointx = models.FloatField(db_column='WaypointX', blank=True, null=True)  # Field name made lowercase.
    waypointtimearrived = models.DateTimeField(db_column='WaypointTimeArrived', blank=True, null=True)  # Field name made lowercase.
    mission_missionid = models.ForeignKey(Mission, models.DO_NOTHING, db_column='Mission_MissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Waypoint'
        unique_together = (('waypointid', 'mission_missionid'),)
        app_label = "Waypoint"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'
        app_label = "auth_group"


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)
        app_label = "auth_group_permissions"


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)
        app_label = "auth_permission"


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
        app_label = "auth_user"


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)
        app_label = "auth_user_groups"


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)
        app_label = "auth_user_user_permissions"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'
        app_label = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
        app_label = "django_content_type"


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
        app_label = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
        app_label = "django_session"
