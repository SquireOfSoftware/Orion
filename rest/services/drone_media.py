#!/usr/bin/env python
import rospy
import cv2
import logging
import base64
import numpy as np
from datetime import datetime, date, time
from sensor_msgs.msg import Image
from database_access_layer import *
from resource_locator import resource_locator, resource
from cv_bridge import CvBridge, CvBridgeError



class drone_media(resource):
    def __init__(self, resource_locator):
        super(drone_media, self).__init__(resource_locator)
        rospy.init_node('orion_image_reader', anonymous=True)
        self.image_sub = rospy.Subscriber("ardrone/image_raw", Image, self.image_callback)
        self.bridge = CvBridge()
        self.cv2_img = None
        self.img_str = ""
        print "Drone Media Set"
        return

    def image_callback(self, data):
        print "Calling back line 1"
        try:
            self.cv2_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        else:
            img = cv2.imencode('.png', self.cv2_img)[1:]
            print(type(img))
            print(img)
            self.img_str = base64.b64encode(img[0])
            #Write to DB
            now = datetime.now()
            print "Callback"
            values = (now.strftime("%Y-%m-%d %H:%M:%S"), self.img_str) 
            super(drone_media, self).connection().start_transaction(isolation_level='READ COMMITTED')
            sql = "INSERT INTO Image (ImageTimestamp, ImageBlob, Mission_MissionID) VALUES (%s, %s, (SELECT MissionID from Mission WHERE MissionStatus_MissionStatusID = 2 LIMIT 1) );"
            super(drone_media, self).cursor().execute(sql, values)
            super(drone_media, self).connection().commit()
