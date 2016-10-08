#!/user/bin/env python
import roslib
import rospy
import json
import data_access_layer

from ardrone_autonomy.msg import Navdata

class drone_metadata(object):
    def __init__(self, database_access_layer):
        self.jstring = None
        #Extract from ardrone/navdata
        self.subNavdata = rospy.subscribe('/ardrone/navdata', Navdata, self.ReceiveNavdata)
        self.current = None

    #Call back for Navdata Extraction
    def ReceiveNavdata(navdata):
        self.current = {'type' : 'navdata', 'data' : navdata })
        self.jstring = json.dumps(self.current)
        
        #Write to database
        
