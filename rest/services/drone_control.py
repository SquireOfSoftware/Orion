#!usr/bin/env python
import roslib;
import rospy;
from math import pi

from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
import time;
class drone_control (object):

    def __init__(self):
        self._move = rospy.Publisher('/cmd_vel', Twist, queue_size = 20)
        self._land = rospy.Publisher('/ardrone/land', Empty, queue_size = 5)
        self._emergency = rospy.Publisher('/ardrone/emergency', Empty, queue_size = 5)
        self._takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size = 5)
        rospy.init_node('orion_controller', anonymous=True)
        rate = rospy.Rate(60)
        
        #Wait until publisher has starded up.
        rospy.sleep(1)
        


    def land(self):
        self._land.publish(Empty())
        return

    def emergency(self):
        self._emergency.publish(Empty())
        return

    def takeoff(self):
        self._takeoff.publish(Empty())
        return

    # Stops the drone from moving
    def stop(self):
        self.move({'linear':{'x':0,'y':0,'z':0}, 'angular':{'x':0,'y':0,'z':0}})

    def move(self, data):
        self.linear = data['linear']
        self.angular = data['angular']
        self._move.publish(Twist(Vector3(data['linear']['x'],
                                        data['linear']['y'],
                                        data['linear']['z']),
                                Vector3(data['angular']['x'],
                                        data['angular']['y'],
                                        data['angular']['z'])))
    def test(self):
        self.takeoff()
        #Takes more time
        time.sleep(6)
        self.stop()
        time.sleep(1)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(1.0)}})
        #2 Second rotation = 180 at 100%
        #Also very unpredictable
        time.sleep(2)
        self.stop()
        self.sleep(1)
        self.move({'linear':{'x':0.1, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':0}})
        time.sleep(1)
        self.stop()
        time.sleep(1)
        self.move({'linear':{'x':0, 'y':0, 'z':-0.5}, 'angular':{'x':0, 'y':0, 'z':0}})
        time.sleep(1)
        self.stop()
        self.land()

