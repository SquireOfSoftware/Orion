#!/usr/bin/env python
import rospy
import cv2
import logging
from sensor_msgs.msg import Image
from database_access_layer import *
from resource_locator import resource_locator, resource
from cv_bridge import CvBridge, CvBridgeError



class drone_media(connector, resource):
    def __init__(self, resource_locator):
        resource.__init__(resource_locator)
        connector.__init__(resource_locator)
        rospy.init_node('orion_image_reader', anonymous=True)
        self.image_sub = rospy.Subscriber("adrone/image_raw", Image, self.image_callback)
        self.bridge = CvBridge()
        return



    def image_callback(data):
        try:
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError, e:
            print(e)
        else:
            img_str = cv2.imencode('.png', cv2_img)[1].tostring()

        #Write to DB
