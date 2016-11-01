import roslib
import rospy
import json
import time
from copy import deepcopy

from database_access_layer import connector
from drone_control import drone_control
from geometry_msgs.msg import Point
from resource_locator import resource

class drone_mission(connector, resource):
    def __init__(self, resource_locator):
        connector.__init__(self)
        resource.__init__(self)

    def start(self):
        self.connect()
        # Execute check if any mission is in progress
        sql = 'SELECT MissionID FROM Mission WHERE MissionStatus_MissionStatusID = 2;'
        for result in self.cursor.execute(sql):
            #  If nothing is running quit.
            if result.rowcount is 0:
                return False

        # Query to get mission. Get all waypoints
        sql = """SELECT
                        Waypoint.*, Mission.MissionAltitude
                    FROM
                        Waypoint
                            INNER JOIN
                        Mission ON Waypoint.Mission_MissionID = Mission.MissionID
                    WHERE
                        Mission.MissionStatus_MissionStatusID = 2
                    ORDER BY WaypointID ASC;"""
        way_first = None
        result_set = deepcopy(self.cursor.execute(sql))
        for result in result_set:
            if way_first is None:
                # Grab waypoints (which are in cm) and convert into meters
                way_first = Point()
                way_first.x = result['WaypointX']/100
                way_first.y = result['WaypointY']/100
                way_first.z = result['MissionAltitude']

                # Update the waypoint element with the current time
                arrived_at_waypoint_sql = 'UPDATE Waypoint SET WaypointTimeArrived = NOW() WHERE WaypointID = ' + result['WaypointID']
                self.cursor.execute(arrived_at_waypoint_sql)
                continue
            else:
                # Grab waypoints (which are in cm) and convert into meters
                way_second = Point()
                way_second.x = result['WaypointX']/100
                way_second.y = result['WaypointY']/100
                way_second.z = result['MissionAltitude']/100

                # Since we have two waypoints, initiate a move
                drone_control.moveQuantum(self, way_first, way_second)

                # Update the waypoint element with the current time
                arrived_at_waypoint_sql = 'UPDATE Waypoint SET WaypointTimeArrived = NOW() WHERE WaypointID = ' + result['WaypointID']
                self.cursor.execute(arrived_at_waypoint_sql)

                # We have moved to the second waypoint, so iterate to the next point
                way_first = way_second

