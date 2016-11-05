#!/user/bin/env python
import roslib
import rospy
import json
import time
from database_access_layer import connector
from datetime import date, datetime, timedelta
from resource_locator import resource, resource_locator
from mysql import *
from ardrone_autonomy.msg import Navdata
# Define insert statements here
next_data =  "INSERT INTO Metadata (MetadataTimestamp, Drone_DroneID, MetadataBattery, MetadataState, MetadataMagX, MetadataMagY, MetadataMagZ, MetadataPressure, MetadataTemp, MetadataWindSpeed, MetadataWindAngle, MetadataWindCompAngle, MetadataRotX, MetadataRotY, MetadataRotZ, MetadataAltd, MetadataVX, MetadataVY, MetadataVZ, MetadataAX, MetadataAY, MetadataAZ, MetadataMotor1, MetadataMotor2, MetadataMotor3, MetadataMotor4, MetadataTM) \
VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


class drone_metadata(resource):
    def __init__(self, resource_locator):
        super(drone_metadata, self).__init__(resource_locator)
        self.jstring = None
        #Extract from ardrone/navdata
        self.subNavdata = rospy.Subscriber('/ardrone/navdata', Navdata, self.ReceiveNavdata)
        self.current = None
        

    #Call back for Navdata Extraction
    def ReceiveNavdata(self, navdata):
        navdata = navdata  # type: Navdata

        #super(drone_metadata, self).connection().start_transaction()
        
        #Write jstring to database
        self.timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # FIXME: we need to get the proper droneID here -- MattHa 2016-10-05
        data_navdata = (
            self.timenow,
            1,
            navdata.batteryPercent,
            navdata.state,
            navdata.magX,
            navdata.magY,
            navdata.magZ,
            navdata.pressure,
            navdata.temp,
            navdata.wind_speed,
            navdata.wind_angle,
            navdata.wind_comp_angle,
            navdata.rotX,
            navdata.rotY,
            navdata.rotZ,
            navdata.altd,
            navdata.vx,
            navdata.vy,
            navdata.vz,
            navdata.ax,
            navdata.ay,
            navdata.az,
            navdata.motor1,
            navdata.motor2,
            navdata.motor3,
            navdata.motor4,
            navdata.tm
        )

        sql = "INSERT INTO Image (ImageTimestamp, ImageBlob, Mission_MissionID) VALUES" \
              " (%s, %s, %s);"
        dictionary = {
            'imageTimestamp': self.timenow,
            'imageBlob': " ",
            'mission_MissionID': 3,
        }
        #super(drone_metadata, self).cursor().execute()
        #super(drone_metadata, self).cursor().execute(sql, (self.timenow, " ", 3))

        #select_stmt = "SELECT * FROM Mission WHERE MissionId = %s"
        #super(drone_metadata, self).cursor().execute(select_stmt, (3,))
        #super(drone_metadata, self).connection().paramstyle = 'pyformat'
        super(drone_metadata, self).cursor().execute(next_data, data_navdata)

        super(drone_metadata, self).connection().commit()
