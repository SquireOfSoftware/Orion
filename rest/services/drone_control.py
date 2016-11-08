#!usr/bin/env python
import time
from copy import deepcopy
from math import atan2
from math import degrees
from math import hypot

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from nav_msgs.msg import Odometry
from std_msgs.msg import Empty

from resource_locator import resource


# from sensor_msgs.msg import LaserScan


class drone_control(resource):
    # Note, max recommended speed is 0.8
    ROT_SPEED = 0.5
    ROTATION_ERROR = 2
    NAVIGATIONAL_POLLING_SLEEP = 0.1
    LIN_SPEED = 0.08
    LIN_SPEED_MIN_PERCENTAGE = 0.1
    POSITIONAL_ERROR = 1
    DISTANCE_POLLING_SLEEP = 0.1

    def __init__(self, resource_locator):
        super(drone_control, self).__init__(resource_locator)
        self._move = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        self._land = rospy.Publisher('/ardrone/land', Empty, queue_size=5)
        self._emergency = rospy.Publisher('/ardrone/emergency', Empty, queue_size=5)
        self._takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=5)
        self._odometry = rospy.Subscriber('/ardrone/odometry', Odometry, self.odom_callback)
        rospy.init_node('orion_controller', anonymous=True)
        rate = rospy.Rate(60)

        # Wait until publisher has started up.
        rospy.sleep(2)

    def land(self):
        self._land.publish(Empty())
        #super(resource, self).cursor
        return

    def emergency(self):
        self._emergency.publish(Empty())
        return

    def takeoff(self):
        self._takeoff.publish(Empty())
        return

    # Stops the drone from moving
    def stop(self):
        self.move({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})

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
        capped_speed = self.LIN_SPEED * speed_ratio
        if capped_speed > self.LIN_SPEED:
            capped_speed = self.LIN_SPEED
        self.move({'linear': {'x': capped_speed, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})

    def rotate_to_face_point(self, drone_location, target_location):
        """
        Receives the drone's location and attempts to rotate it towards the given target_location
        @:type self: drone_control
        @:type drone_location: Point
        @:type target_location: Point
        """
        print "DEBUG: ~~~ "
        print "DEBUG: entering rotate_to_face_point"
        relative_goal_x = target_location.x - drone_location.x
        relative_goal_y = target_location.y - drone_location.y

        target_angle = degrees(atan2(relative_goal_x, relative_goal_y))
        print "DEBUG rotate x: " + str(relative_goal_x) + " y: " + str(relative_goal_y) + " ang: " + str(target_angle)

        count = 0
        drone_meta = super(drone_control, self).locator().getDroneMetadata()
        # Rotate until we are facing the right direction
        while True:
            nav_data = drone_meta.navdata()

            current_direction = nav_data.rotZ  # Float degrees
            rotational_difference = target_angle - current_direction

            if rotational_difference < -180:
                rotational_difference += 360

            if rotational_difference > self.ROTATION_ERROR:
                self.rotate_clockwise()
            elif rotational_difference < -self.ROTATION_ERROR:
                self.rotate_anticlockwise()
            else:
                break
            count += 1
            time.sleep(self.NAVIGATIONAL_POLLING_SLEEP)

            if ((count % 10) == 0) or (count == 1):
                print "DEBUG: rot count " + str(count)
                print "DEBUG: current direction " + str(current_direction)
                print "DEBUG: difference  " + str(rotational_difference)
                print "DEBUG: ~~~"

            if count > 150:
                # FIXME make sure to remove this
                print "DEBUG: rotated " + str(count) + " times"
                break

        # Stop rotating
        self.stop()
        self.stop()
        time.sleep(2)
        print "DEBUG: finished rotation ~~~~~~~~~~~~~~~~"
        print "DEBUG: current direction " + str(current_direction)
        print "DEBUG: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.stop()
        self.stop()
        print "DEBUG: sleeping 3s"
        print "DEBUG: "
        time.sleep(3)

    # start and end are geometry_msgs Points
    def moveQuantum(self, start, end):
        """
        @:type self: drone_control
        @:type start: Point
        @:type end: Point
        """
        print "DEBUG: ... "
        print "DEBUG: entering moveQuantam"

        self.rotate_to_face_point(start, end)
        print "DEBUG: --------------- "
        print "DEBUG: STARTING MOVE"
        relative_goal_x = end.x - start.x
        relative_goal_y = end.y - start.y
        total_distance = hypot(relative_goal_x, relative_goal_y)

        print "DEBUG: total_distance " + str(total_distance)
        # print "DEBUG: odom object " + str(self.odometry)

        starting_distance_moved = deepcopy(self.odometry.pose.pose.position.x)
        goal_distance = starting_distance_moved + total_distance

        print "DEBUG: starting_distance_moved " + str(starting_distance_moved)
        print "DEBUG: goal_distance " + str(goal_distance)
        print "DEBUG: --------------- "

        count = 0
        while True:
            current_distance = self.odometry.pose.pose.position.x

            if current_distance <= goal_distance:
                # Go forward, but slow down as we approach the target, minimum 10% of LIN_SPEED
                speed_ratio = (current_distance / goal_distance) + self.LIN_SPEED_MIN_PERCENTAGE
                self.move_at_speed(speed_ratio)
                if ((count % 10) == 0) or (count == 1):
                    print "DEBUG: Trying to move RATIO " + str(speed_ratio)
                    print "DEBUG: Trying to move at speed " + str(self.LIN_SPEED * speed_ratio)

                count += 1
                time.sleep(self.DISTANCE_POLLING_SLEEP)

            elif current_distance > goal_distance + self.POSITIONAL_ERROR:
                print "DEBUG: Moved too far, go backwards. Cur: " + str(current_distance) + \
                      " goal: " + str(goal_distance)
                # Moved too far, so go backwards at the minimum speed
                self.move_at_speed(-self.LIN_SPEED_MIN_PERCENTAGE)
                count += 1
                time.sleep(self.DISTANCE_POLLING_SLEEP)

            else:
                # We arrived!
                print "DEBUG: "
                print "DEBUG: We arrived at the point"
                print "DEBUG: current distance " + str(current_distance)
                print "DEBUG: "
                self.stop()
                self.stop()
                break

            if ((count % 10) == 0) or (count == 1):
                print "DEBUG: count " + str(count)
                print "DEBUG: current distance " + str(current_distance)
                print "DEBUG: goal_distance  " + str(goal_distance)

            if count > 30:
                # FIXME make sure to remove this
                print "DEBUG: tried to move " + str(count) + " times"
                break

        self.stop()
        self.stop()
        time.sleep(2)

    def test(self):
        self.takeoff()
        # Takes more time
        time.sleep(8)
        self.move({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
        time.sleep(0.2)
        self.stop()
        time.sleep(0.2)
        self.stop()
        time.sleep(0.2)
        self.stop()
        time.sleep(1)
        # self.move({'linear':{'x': 0, 'y': 0, 'z': 0}, 'angular':{'x': 0, 'y': 0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        # self.move({'linear':{'x': 0, 'y': 0, 'z': 0}, 'angular':{'x': 0, 'y': 0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        # self.move({'linear':{'x': 0, 'y': 0, 'z': 0}, 'angular':{'x': 0, 'y': 0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        # self.move({'linear':{'x': 0, 'y': 0, 'z': 0}, 'angular':{'x': 0, 'y': 0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        # self.move({'linear':{'x': 0, 'y': 0, 'z': 0}, 'angular':{'x': 0, 'y': 0, 'z':(0.5)}})
        time.sleep(0.3)
        self.stop()
        time.sleep(0.4)
        # self.move({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z':(0.5)}})
        time.sleep(0.2)
        # 2 Second rotation = 180 at 100%
        # Also very unpredictable
        self.stop()
        time.sleep(1)
        self.move({'linear': {'x': 0.1, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
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
        self.move({'linear': {'x': 0.1, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
        time.sleep(2)
        self.stop()
        time.sleep(2)
        self.move({'linear': {'x': -0.1, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
        time.sleep(2)
        self.stop()
        time.sleep(2)
        self.land()

    def odom_callback(self, data):
        self.odometry = data
