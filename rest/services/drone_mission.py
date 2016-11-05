import roslib
import rospy
import json
import sys
import time
from copy import deepcopy

from database_access_layer import connector
from drone_control import drone_control
from geometry_msgs.msg import Point
from resource_locator import resource
from sensor_msgs.msg import LaserScan


class drone_mission(resource):
    def __init__(self, resource_locator):
        super(drone_mission, self).__init__(resource_locator)

    def start_test(self):
        self.connect()
        drone_control_object = super(drone_mission, self).locator().getDroneControl()

        drone_control_object.takeoff()
        time.sleep(4)
        drone_control_object.stop()
        drone_control_object.stop()
        time.sleep(5)
        drone_control_object.land()
        exit()

    def start(self):
        self.connect()
        drone_control_object = super(drone_mission, self).locator().getDroneControl()

        # Check to see if there is a mission IN PROGRESS, and try to get its ID
        get_mission_sql = 'SELECT MissionID FROM Mission WHERE MissionStatus_MissionStatusID = 2;'
        cursor = super(drone_mission, self).cursor()
        cursor.execute(get_mission_sql)
        data = cursor.fetchone()
        if data is None:
            print "Cannot find mission in the IN PROGRESS status"
            raise Exception('Cannot find mission in the IN PROGRESS status')
        else:
            mission_id = data[0]
            print "Launching Mission: " + str(mission_id)

        # Query to get mission. Get all waypoints
        sql = """SELECT
                        Waypoint.WaypointID, Waypoint.WaypointX, Waypoint.WaypointY, Mission.MissionAltitude
                    FROM
                        Waypoint
                            INNER JOIN
                        Mission ON Waypoint.Mission_MissionID = Mission.MissionID
                    WHERE
                        Mission.MissionStatus_MissionStatusID = 2
                    ORDER BY WaypointID ASC;"""
        way_first = None
        try:
            cursor.execute(sql)

            result_set = deepcopy(cursor.fetchall())
            for result in result_set:
                if way_first is None:
                    # Grab waypoints (which are in cm) and convert into meters
                    way_first = Point()
                    way_first.x = result[1]/100
                    way_first.y = result[2]/100
                    way_first.z = result[3]/100

                    print "DEBUG: Waypoint 1"
                    print str(way_first)

                    # Update the waypoint element with the current time
                    arrived_at_waypoint_sql = 'UPDATE Waypoint SET WaypointTimeArrived = NOW() WHERE WaypointID = ' + str(result[0]) + ';'
                    cursor.execute(arrived_at_waypoint_sql)

                    # Take off and wait 5 sec.
                    drone_control_object.takeoff()
                    time.sleep(5)
                    drone_control_object.stop()
                    continue
                else:
                    # Grab waypoints (which are in cm) and convert into meters
                    way_second = Point()
                    way_second.x = result[1]/100
                    way_second.y = result[2]/100
                    way_second.z = result[3]/100

                    print "DEBUG: Waypoint 2"
                    print str(way_second)

                    # Since we have two waypoints, initiate a move
                    drone_control_object.moveQuantum(way_first, way_second)

                    # Update the waypoint element with the current time
                    arrived_at_waypoint_sql = 'UPDATE Waypoint SET WaypointTimeArrived = NOW() WHERE WaypointID = ' + str(result[0]) + ';'
                    cursor.execute(arrived_at_waypoint_sql)

                    # We have moved to the second waypoint, so iterate to the next point
                    way_first = way_second
            # Mission is finished
            print "DEBUG: Mission is finished"
            drone_control_object.land()
            complete_mission_sql = 'UPDATE Mission SET MissionStatus_MissionStatusID = 4 WHERE MissionID = ' + str(mission_id) + ';'
            cursor.execute(complete_mission_sql)

        except (KeyboardInterrupt, SystemExit):

            drone_control_object.land()
            abort_mission_sql = 'UPDATE Mission SET MissionStatus_MissionStatusID = 3 WHERE MissionID = ' + str(mission_id) + ';'
            cursor.execute(abort_mission_sql)

            raise
        except:
            # ttributeError: 'MySQLCursorPrepared' object has no attribute 'commit'
            drone_control_object.land()
            abort_mission_sql = 'UPDATE Mission SET MissionStatus_MissionStatusID = 3 WHERE MissionID = ' + str(mission_id) + ';'
            # cursor.execute(abort_mission_sql)
            print "Unexpected error:", sys.exc_info()[0]
            raise
