#!usr/bin/env python
import roslib;
import rospy;

from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
class drone_control (object):
    def __init__(self):
        self.move = rospy.Publisher('/cmd_vel', Twist, queue_size = 20)
        self.land = rospy.Publisher('/ardrone/land', Empty, queue_size = 5)
        self.emergency = rospy.Publisher('/ardrone/emergency', Empty, queue_size = 5)
        self.takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size = 5)
        rospy.init_node('orion_controller', anonymous=True)
        rate = rospy.Rate(100)


    def drone_land(self):
        self.land.publish(Empty())
        return

    def drone_emergency(self):
        self.emergency.publish(Empty())
        return

    def drone_takeoff(self):
        self.takeoff.publish(Empty())
        return

    def drone_move(self, data):
        self.linear = data.linear
        self.angular = data.angular
        self.move.publish(Twist(Vector3(data.linear.x,
                                        data.linear.y,
                                        data.linear.z),
                                Vector3(data.angular.x,
                                        data.angular.y,
                                        data.angular.z)))
