#!usr/bin/env python
import roslib;
import rospy;
from math import pi
from math import atan2
from math import degrees
from math import hypot
from math import radians

from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Point
import time;
class drone_control (object):

    def __init__(self):
        self._move = rospy.Publisher('/cmd_vel', Twist, queue_size = 40)
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

    # start and end are geometry_msgs Points
    def moveQuantum(self, start, end):
        # type: (drone_control, Point, Point) -> None

        arbitrary_turn_seconds = 2
        arbitrary_travel_seconds = 2

        # Double check that the Point coords can be accessed like this
        x = end.x - start.x
        y = end.y - start.y
        distance = hypot(x, y)
        new_direction = degrees(atan2(x, y))

        # FIXME need to check the navdata topic for info on current rotation in degrees
        current_direction = 0 # get from Nav data, rotz (degrees)

        total_rotation = new_direction - current_direction

        total_rotation_speed = radians(total_rotation) / arbitrary_turn_seconds

        # Turn
        self.move({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': total_rotation_speed}})
        time.sleep(arbitrary_turn_seconds)

        # Move forward
        self.move({'linear': {'x': distance, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
        time.sleep(arbitrary_travel_seconds) # TODO check the speed? not just distance

        # TODO implement a check vs the speed and the position the drone thinks its in.

    def test(self):
        self.takeoff()
        #Takes more time
        time.sleep(8)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0)}})
        time.sleep(0.2)
        self.stop()
        time.sleep(0.2)
        self.stop()
        time.sleep(0.2)
        self.stop()
        time.sleep(1)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.2)
        #2 Second rotation = 180 at 100%
        #Also very unpredictable
        self.stop()
        time.sleep(1)
        self.move({'linear':{'x':0.1, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':0}})
        time.sleep(1)
        self.stop()
        time.sleep(1)
        self.move({'linear':{'x':0, 'y':0, 'z':-0.5}, 'angular':{'x':0, 'y':0, 'z':0}})
        time.sleep(1)
        self.stop()
        self.land()

