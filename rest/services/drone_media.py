#!/usr/bin/env python
import rospy
import cv2
import logging
import base64
from datetime import datetime, date, time
from sensor_msgs.msg import Image
from database_access_layer import *
from resource_locator import resource_locator, resource
from cv_bridge import CvBridge, CvBridgeError



class drone_media(resource):
    def __init__(self, resource_locator):
        super(drone_media, self).__init__(resource_locator)
        rospy.init_node('orion_image_reader', anonymous=True)
        self.image_sub = rospy.Subscriber("adrone/image_raw", Image, self.image_callback)
        self.bridge = CvBridge()
        print "Test"
        return

    def image_callback(data):
        try:
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError, e:
            print(e)
        
        img = cv2.imencode('.png', cv2_img)[1:]
        img_str = base64.b64encode(img)
        #Write to DB
        now = dateime.now()
        print img_str
        data = (now.strftime("%Y-%m-%d %H:%M:%S"), img_str) 
        super(resource, self).connection.start_transaction(isolation_level='READ COMMITED')
        sql = "INSERT INTO Image (ImageTimestamp, ImageBlob, Mission_MissionID) VALUES (%s, %s, (SELECT MissionID from Mission WHERE MissionStatus_MissionStatusID = 2 LIMIT 1) );"
        super(resource, self).cursor.execute(sql, data)
        super(resource, self).connection.commit()
