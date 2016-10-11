#!/user/bin/env python
import roslib
import rospy
import json
from database_access_layer import Connector
from datetime import date, datetime, timedelta

from ardrone_autonomy.msg import Navdata
# Define insert statements here

class drone_metadata(Connector):
    def __init__(self, database_access_layer):
        self.jstring = None
        #Extract from ardrone/navdata
        self.subNavdata = rospy.subscribe('/ardrone/navdata', Navdata, self.ReceiveNavdata)
        self.current = None

    #Call back for Navdata Extraction
    def ReceiveNavdata(self, navdata):

        self.current = {'data' : navdata }
        self.jstring = json.dumps(self.current)
        
        #Write jstring to database
        self.timenow = datetime.date()




