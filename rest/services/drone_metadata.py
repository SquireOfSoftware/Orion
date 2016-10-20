#!/user/bin/env python
import roslib
import rospy
import json
from database_access_layer import connector
from datetime import date, datetime, timedelta
from resource_locator import resource, resource_locator

from ardrone_autonomy.msg import Navdata
# Define insert statements here
next_data = ("INSERT INTO Metadata"
             "(MetadataBlob, MetadataTimestamp, Drone_DroneID) "
             "VALUES (%(MetadataBlob), %(MetadataTimestamp), %(Drone_DroneID) 


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
        self.timenow = datetime.date()




