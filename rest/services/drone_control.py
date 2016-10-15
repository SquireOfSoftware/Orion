#!usr/bin/env python
import roslib;
import rospy;

from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from std_msgs.msg import Vector3
class drone_control (object):
    def __init__(self):
        self.move = rospy.Publisher('/cmd_vel', Twist, queue_size = 20)
        self.land = rospy.Publisher('/ardrone/Land', Empty, queue_size = 5)
        self.emergency = rospy.Publisher('/ardrone/Emergency', Empty, queue_size = 5)
        self.takeoff = rospy.Publisher('/ardrone/TakeOff', Empty, queue_size = 5)

        return

    def drone_land(self):
        self.land.publish(std_msgs.msg.Empty())
        pass

    def drone_emergency(self):
        self.emergency.publish(std_msgs.msg.Empty())
        pass

    def drone_takeoff(self):
        self.emergency.publish(std_msgs.msg.Empty())
        pass

    def drone_move(self, data):
        self.linear = data.linear
        self.angular = data.angular
        self.move.publish(Twist(Vector3(data.linear.x,
                                        data.linear.y,
                                        data.linear.z),
                                Vector3(data.angular.x,
                                        data.angular.y,
                                        data.angular.z)))