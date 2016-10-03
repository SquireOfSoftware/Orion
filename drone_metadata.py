#!/user/bin/env python
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy;
import json;

from ardrone_autonomy.msg import Navdata;
import PDO;

class DroneMetadata(object):
    def __init__(self):
        self.jstring = None
        #Extract from ardrone/navdata
        self.subNavdata = rospy.subscribe('/ardrone/navdata', Navdata, self.ReceiveNavdata)
        
        #Establish PDO Connection


    #Call back for Navdata Extraction
    def ReceiveNavdata(navdata):
        self.jstring = json.dumps({ 'type': 'navdata', 'data' : navdata})
        
        #Write to database
    

