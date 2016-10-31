# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from management_constants import MISSION_STATUS
from management_constants import DRONE_STATUS


def convert_mission_status(id):
    for key, value in MISSION_STATUS.iteritems():
        if value == id:
            return key.replace("_", " ")
    return None


def convert_drone_status(id):
    for key, value in DRONE_STATUS.iteritems():
        if value == id:
            return key
    return None


class DroneStatus(models.Model):
    dronestatusid = models.AutoField(db_column='DroneStatusID',
                                     primary_key=True)  # Field name made lowercase.
    dronestatusname = models.CharField(db_column='DroneStatusName',
                                       max_length=45,
                                       blank=True,
                                       null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DroneStatus'
        app_label = 'DroneStatus'

    def as_dict(self):
        return {
            "id": self.dronestatusid,
            "status": self.dronestatusname
        }


class Drone(models.Model):
    droneid = models.AutoField(db_column='DroneID', primary_key=True)  # Field name made lowercase.
    dronename = models.CharField(db_column='DroneName',
                                 max_length=10,
                                 blank=True,
                                 null=True)  # Field name made lowercase.
    droneip = models.CharField(db_column='DroneIP',
                               max_length=16,
                               blank=True,
                               null=True)  # Field name made lowercase.
    dronestatus_dronestatusid = models.ForeignKey(DroneStatus,
                                                  on_delete=models.DO_NOTHING,
                                                  db_column='DroneStatus_DroneStatusID',
                                                  null=False) # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Drone'
        app_label = "Drone"

    def as_dict(self):
        return {
            "id": self.droneid,
            "ip": self.droneip,
            "name": self.dronename,
            "status": convert_drone_status(int(self.dronestatus_dronestatusid.dronestatusid))
        }

    def get_status(self):
        return convert_drone_status(int(self.dronestatus_dronestatusid.dronestatusid))


class Missionstatus(models.Model):
    missionstatusid = models.AutoField(db_column='MissionStatusID',
                                       primary_key=True)  # Field name made lowercase.
    missionstatusname = models.CharField(db_column='MissionStatusName',
                                         max_length=45,
                                         blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MissionStatus'
        app_label = "MissionStatus"

    def as_dict(self):
        return {
            "id": self.missionstatusid,
            "status": self.missionstatusname
        }


class Mission(models.Model):
    missionid = models.AutoField(db_column='MissionID',
                                    primary_key=True)  # Field name made lowercase.
    missionstarttime = models.DateTimeField(db_column='MissionStartTime',
                                            blank=True,
                                            null=True)  # Field name made lowercase.
    missionendtime = models.DateTimeField(db_column='MissionEndTime',
                                          blank=True,
                                          null=True)  # Field name made lowercase.
    missioncreationdate = models.DateTimeField(db_column='MissionCreationDate')  # Field name made lowercase.
    missionaltitude = models.FloatField(db_column='MissionAltitude',
                                        blank=True,
                                        null=True)  # Field name made lowercase.
    missionstatus_missionstatusid = models.ForeignKey(Missionstatus,
                                                       on_delete=models.DO_NOTHING,
                                                       db_column='MissionStatus_MissionStatusID',
                                                       blank=True,
                                                       null=True)  # Field name made lowercase.
    drone_droneid = models.ForeignKey(Drone,
                                      on_delete=models.DO_NOTHING,
                                      db_column='Drone_DroneID',
                                      blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mission'
        app_label = "Mission"

    def as_dict(self):
        mission_status_id = ""
        drone_id = ""
        if self.missionstatus_missionstatusid is None:
            mission_status_id = MISSION_STATUS["QUEUED"]
        else:
            mission_status_id = self.missionstatus_missionstatusid.missionstatusid

        if self.drone_droneid is None:
            drone_id = -1
        else:
            drone_id = self.drone_droneid.droneid

        return {
            "id": self.missionid,
            "start_time": self.missionstarttime.__str__(),
            "end_time": self.missionendtime.__str__(),
            "creation_date": self.missioncreationdate.__str__(),
            "altitude": self.missionaltitude,
            "status": convert_mission_status(int(mission_status_id)),
            "drone_id": drone_id
        }


class Metadata(models.Model):
    metadataid = models.IntegerField(db_column='MetadataID',
                                     primary_key=True)  # Field name made lowercase.
    metadatabattery = models.FloatField(db_column="MetadataBattery",
                                        blank=True,
                                        null=True)
    metadatastate = models.IntegerField(db_column="MetadataState",
                                        blank=True,
                                        null=True)
    metadatamagx = models.FloatField(db_column="MetadataMagX",
                                     blank=True,
                                     null=True)
    metadatamagy = models.FloatField(db_column="MetadataMagY",
                                     blank=True,
                                     null=True)
    metadatamagz = models.FloatField(db_column="MetadataMagZ",
                                     blank=True,
                                     null=True)
    metadatapressure = models.IntegerField(db_column="MetadataPressure",
                                           blank=True,
                                           null=True)
    metadatatemp = models.IntegerField(db_column="MetadataTemp",
                                       blank=True,
                                       null=True)
    metadatawindspeed = models.IntegerField(db_column="MetadataWindSpeed",
                                            blank=True,
                                            null=True)
    metadatawindangle = models.IntegerField(db_column="MetadataWindAngle",
                                            blank=True,
                                            null=True)
    metadatawindcompangle = models.IntegerField(db_column="MetadataWindCompAngle",
                                            blank=True,
                                            null=True)
    metadatarotx = models.FloatField(db_column="MetadataRotX",
                                     blank=True,
                                     null=True)
    metadataroty = models.FloatField(db_column="MetadataRotY",
                                     blank=True,
                                     null=True)
    metadatarotz = models.FloatField(db_column="MetadataRotZ",
                                     blank=True,
                                     null=True)
    metadataaltitude = models.IntegerField(db_column="MetadataAltd",
                                           blank=True,
                                           null=True)
    metadatavx = models.FloatField(db_column="MetadataVX",
                                   blank=True,
                                   null=True)
    metadatavy = models.FloatField(db_column="MetadataVY",
                                   blank=True,
                                   null=True)
    metadatavz = models.FloatField(db_column="MetadataVZ",
                                   blank=True,
                                   null=True)
    metadataax = models.FloatField(db_column="MetadataAX",
                                   blank=True,
                                   null=True)
    metadataay = models.FloatField(db_column="MetadataAY",
                                   blank=True,
                                   null=True)
    metadataaz = models.FloatField(db_column="MetadataAZ",
                                   blank=True,
                                   null=True)
    metadatamotor1 = models.IntegerField(db_column="MetadataMotor1",
                                         blank=True,
                                         null=True)
    metadatamotor2 = models.IntegerField(db_column="MetadataMotor2",
                                         blank=True,
                                         null=True)
    metadatamotor3 = models.IntegerField(db_column="MetadataMotor3",
                                         blank=True,
                                         null=True)
    metadatamotor4 = models.IntegerField(db_column="MetadataMotor4",
                                         blank=True,
                                         null=True)
    metadatatm = models.FloatField(db_column="MetadataTM",
                                   blank=True,
                                   null=True)
    metadatatimestamp = models.DateTimeField(db_column='MetadataTimestamp',
                                             blank=True,
                                             null=True)  # Field name made lowercase.
    drone_droneid = models.ForeignKey(Drone,
                                      on_delete=models.DO_NOTHING,
                                      db_column='Drone_DroneID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Metadata'
        unique_together = (('metadataid', 'drone_droneid'),)
        app_label = "Metadata"

    def as_dict(self):
        return {
            "id": self.metadataid,
            "battery": self.metadatabattery,
            "state": self.metadatastate,
            "mag": {
                "x": self.metadatamagx,
                "y": self.metadatamagy,
                "z": self.metadatamagz
            },
            "pressure": self.metadatapressure,
            "temp": self.metadatatemp,
            "wind": {
                "speed": self.metadatawindspeed,
                "angle": self.metadatawindangle,
                "comp_angle": self.metadatawindcompangle
            },
            "rot": {
                "x": self.metadatarotx,
                "y": self.metadataroty,
                "z": self.metadatarotz
            },
            "altitude": self.metadataaltitude,
            "v": {
                "x": self.metadatavx,
                "y": self.metadatavy,
                "z": self.metadatavz
            },
            "a": {
                "x": self.metadataax,
                "y": self.metadatavy,
                "z": self.metadatavz
            },
            "motors": {
                "1": self.metadatamotor1,
                "2": self.metadatamotor2,
                "3": self.metadatamotor3,
                "4": self.metadatamotor4
            },
            "tm": self.metadatatm,
            "timestamp": self.metadatatimestamp.__str__(),
            "drone_id": self.drone_droneid.droneid
        }


class Image(models.Model):
    imageid = models.IntegerField(db_column='ImageID',
                                  primary_key=True)  # Field name made lowercase.
    imagetimestamp = models.DateTimeField(db_column='ImageTimestamp',
                                          blank=True,
                                          null=True)  # Field name made lowercase.
    imageblob = models.TextField(db_column='ImageBlob',
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    mission_missionid = models.ForeignKey(Mission,
                                          on_delete=models.DO_NOTHING,
                                          db_column='Mission_MissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Image'
        unique_together = (('imageid', 'mission_missionid'),)
        app_label = "Image"

    def as_dict(self):
        return {
            "id": self.imageid,
            "timestamp": self.imagetimestamp.__str__(),
            "imageblob": self.imageblob,
            "mission_id": self.mission_missionid.missionid
        }


class Obstacle(models.Model):
    obstacleid = models.IntegerField(db_column='ObstacleID',
                                     primary_key=True)  # Field name made lowercase.
    obstaclecoordinatex = models.FloatField(db_column='ObstacleCoordinateX',
                                            blank=True,
                                            null=True)  # Field name made lowercase.
    obstaclecoordinatey = models.FloatField(db_column='ObstacleCoordinateY',
                                            blank=True,
                                            null=True)  # Field name made lowercase.
    mission_missionid = models.ForeignKey(Mission,
                                          on_delete=models.DO_NOTHING,
                                          db_column='Mission_MissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Obstacle'
        unique_together = (('obstacleid', 'mission_missionid'),)
        app_label = "Obstacle"

    def as_dict(self):
        return {
            "id": self.obstacleid,
            "x": self.obstaclecoordinatex,
            "y": self.obstaclecoordinatey,
            "mission_id": self.mission_missionid.missionid
        }


class Pointofinterest(models.Model):
    pointofinterestid = models.IntegerField(db_column='PointOfInterestIDPointOfInterestID',
                                            primary_key=True)  # Field name made lowercase.
    pointofinterestx = models.FloatField(db_column='PointOfInterestX',
                                         blank=True,
                                         null=True)  # Field name made lowercase.
    pointofinteresty = models.FloatField(db_column='PointOfInterestY',
                                         blank=True,
                                         null=True)  # Field name made lowercase.
    mission_missionid = models.ForeignKey(Mission,
                                          on_delete=models.DO_NOTHING,
                                          db_column='Mission_MissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PointOfInterest'
        unique_together = (('pointofinterestid', 'mission_missionid'),)
        app_label = "PointOfInterest"

    def as_dict(self):
        return {
            "id": self.pointofinterestid,
            "x": self.pointofinterestx,
            "y": self.pointofinteresty,
            "mission_id": self.mission_missionid.missionid
        }


class Waypoint(models.Model):
    waypointid = models.IntegerField(db_column='WaypointID',
                                     primary_key=True)  # Field name made lowercase.
    waypointy = models.FloatField(db_column='WaypointY',
                                  blank=True,
                                  null=True)  # Field name made lowercase.
    waypointx = models.FloatField(db_column='WaypointX',
                                  blank=True,
                                  null=True)  # Field name made lowercase.
    waypointtimearrived = models.DateTimeField(db_column='WaypointTimeArrived',
                                               blank=True,
                                               null=True)  # Field name made lowercase.
    mission_missionid = models.ForeignKey(Mission,
                                          on_delete=models.DO_NOTHING,
                                          db_column='Mission_MissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Waypoint'
        unique_together = (('waypointid', 'mission_missionid'),)
        app_label = "Waypoint"

    def as_dict(self):
        return {
            "id": self.waypointid,
            "x": self.waypointx,
            "y": self.waypointy,
            "time_arrived": self.waypointtimearrived.__str__(),
            "mission_id": self.mission_missionid.missionid
        }


# Useless things that were brought into Django when migrating the db in


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'
        app_label = "auth_group"


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, on_delete=models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)
        app_label = "auth_group_permissions"


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.DO_NOTHING)
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
    user = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)
        app_label = "auth_user_groups"


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, on_delete=models.DO_NOTHING)

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
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING)

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
