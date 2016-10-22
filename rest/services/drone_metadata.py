#!/user/bin/env python
import roslib
import rospy
import json
import time
from database_access_layer import connector
from datetime import date, datetime, timedelta
from resource_locator import resource, resource_locator

from ardrone_autonomy.msg import Navdata
# Define insert statements here
next_data = ("INSERT INTO Metadata"
             "(MetadataBlob, MetadataTimestamp, Drone_DroneID) "
             "VALUES (%(MetadataBlob)s, %(MetadataTimestamp)s, %(Drone_DroneID)s)") 


class drone_metadata(connector, resource):
    def __init__(self, resource_locator):
        connector.__init__()
        resource.__init__()
        self.jstring = None
        #Extract from ardrone/navdata
        self.subNavdata = rospy.subscribe('/ardrone/navdata', Navdata, self.ReceiveNavdata)
        self.current = None
        self.connect()

    #Call back for Navdata Extraction
    def ReceiveNavdata(self, navdata):

        self.current = {'data' : navdata }
        self.jstring = json.dumps(self.current)
        
        #Write jstring to database
        self.timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_navdata = {
            'MetadataBlob' : self.jstring,
            'MetadataTimestamp' : self.timenowm,
            'Drone_DroneID' : 1
        }
        self.cursor.execute(next_data, data_navdata)

        self.connection.commit()
