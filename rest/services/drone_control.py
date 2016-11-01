#!usr/bin/env python
import roslib;
import rospy;
from math import pi
from math import atan2
from math import degrees
from math import hypot
from math import radians
from copy import deepcopy

from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Point
from ardrone_autonomy.msg import Navdata
from nav_msgs.msg import Odometry

import time;
class drone_control (object):
    # Note, max recommended speed is 0.8
    ROT_SPEED = 0.5
    ROTATION_ERROR = 5
    NAVIGATIONAL_POLLING_SLEEP = 0.5
    LIN_SPEED = 0.2
    LIN_SPEED_MIN_PERCENTAGE = 0.1
    POSITIONAL_ERROR = 1
    DISTANCE_POLLING_SLEEP = 0.1

    def __init__(self):
        self._move = rospy.Publisher('/cmd_vel', Twist, queue_size = 40)
        self._land = rospy.Publisher('/ardrone/land', Empty, queue_size = 5)
        self._emergency = rospy.Publisher('/ardrone/emergency', Empty, queue_size = 5)
        self._takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size = 5)
        rospy.init_node('orion_controller', anonymous=True)
        rate = rospy.Rate(60)

        #Wait until publisher has starded up.
        rospy.sleep(2)



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

    def rotate_clockwise(self):
        self.move({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': self.ROT_SPEED}})

    def rotate_anticlockwise(self):
        self.move({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': -self.ROT_SPEED}})

    def move_at_speed(self, speed_ratio):
        self.move({'linear': {'x': self.LIN_SPEED * speed_ratio, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})

    def rotate_to_face_point(self, drone_location, target_location):
        """
        Receives the drone's location and attempts to rotate it towards the given target_location
        @:type self: drone_control
        @:type drone_location: Point
        @:type target_location: Point
        """
        relative_goal_x = target_location.x - drone_location.x
        relative_goal_y = target_location.y - drone_location.y

        target_angle = degrees(atan2(relative_goal_x, relative_goal_y))

        # Rotate until we are facing the right direction
        while True:
            current_direction = Navdata().rotZ  # Float degrees
            rotational_difference = target_angle - current_direction

            if rotational_difference < -180:
                rotational_difference += 360

            if rotational_difference > self.ROTATION_ERROR:
                self.rotate_clockwise()
            elif rotational_difference < -self.ROTATION_ERROR:
                self.rotate_anticlockwise()
            else:
                break

            time.sleep(self.NAVIGATIONAL_POLLING_SLEEP)

        # Stop rotating
        self.stop()

    # start and end are geometry_msgs Points
    def moveQuantum(self, start, end):
        """
        @:type self: drone_control
        @:type start: Point
        @:type end: Point
        """
        self.rotate_to_face_point(start, end)

        relative_goal_x = end.x - start.x
        relative_goal_y = end.y - start.y
        total_distance = hypot(relative_goal_x, relative_goal_y)

        starting_distance_moved = deepcopy(Odometry().pose.pose.position.x)
        goal_distance = starting_distance_moved + total_distance

        while True:
            current_distance = Odometry().pose.pose.position.x

            if current_distance <= goal_distance:
                # Go forward, but slow down as we approach the target, minimum 10% of LIN_SPEED
                speed_ratio = (current_distance/goal_distance) + self.LIN_SPEED_MIN_PERCENTAGE
                self.move_at_speed(speed_ratio)
                time.sleep(self.DISTANCE_POLLING_SLEEP)

            elif current_distance > goal_distance + self.POSITIONAL_ERROR:
                # Moved too far, so go backwards at the minimum speed
                self.move_at_speed(-self.LIN_SPEED_MIN_PERCENTAGE)
                time.sleep(self.DISTANCE_POLLING_SLEEP)

            else:
                # We arrived!
                self.stop()
                break

        self.stop()


    def test(self):
        self.takeoff()
        #Takes more time
        time.sleep(8)
        self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':0}})
        time.sleep(0.2)
        self.stop()
        time.sleep(0.2)
        self.stop()
        time.sleep(0.2)
        self.stop()
        time.sleep(1)
        #self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        #self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        #self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        #self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        #self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        #self.move({'linear':{'x':0, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':(0.5)}})
        time.sleep(0.2)
        #2 Second rotation = 180 at 100%
        #Also very unpredictable
        self.stop()
        time.sleep(1)
        self.move({'linear':{'x':0.1, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':0}})
        time.sleep(1)
        self.stop()
        time.sleep(1)
        time.sleep(1)
        self.stop()
        self.land()

    def test2(self):
        self.takeoff()
        time.sleep(8)
        self.stop()
        time.sleep(2)
        self.move({'linear':{'x':0.1, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':0}})
        time.sleep(2)
        self.stop()
        time.sleep(2)
        self.move({'linear':{'x':-0.1, 'y':0, 'z':0}, 'angular':{'x':0, 'y':0, 'z':0}})
        time.sleep(2)
        self.stop()
        time.sleep(2)
        self.land()
