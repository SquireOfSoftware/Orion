#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from database_access_layer import *
from resource_locator import resource_locator, resource




class drone_media(connector, resource):
    def __init__(self, resource_locator):
        resource.__init__(resource_locator)
        connector.__init__(resource_locator)
        rospy.init_node('image_reader', anonymous=True)
        rospy.Subscriber("adrone/image_raw", Image, self.image_callback)




        return



    def image_callback(data):
        return
