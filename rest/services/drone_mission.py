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

class drone_mission(connector, resource):
    def __init__(self, resource_locator):
        connector.__init__(self)
        resource.__init__(self)

    def start(self):
        self.connect()
        drone_control_object = drone_control()

        # Check to see if there is a mission IN PROGRESS, and try to get its ID
        get_mission_sql = 'SELECT MissionID FROM Mission WHERE MissionStatus_MissionStatusID = 2;'
        self.cursor.execute(get_mission_sql)
        data = self.cursor.fetchone()
        if data is None:
            print "Cannot find mission in the IN PROGRESS status"
            raise Exception('Cannot find mission in the IN PROGRESS status')
        else:
            mission_id = data[0]
            print "Launching Mission: " + mission_id

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
        try:
            self.cursor.execute(sql)
            result_set = deepcopy(self.cursor.fetchall())
            for result in result_set:
                if way_first is None:
                    # Grab waypoints (which are in cm) and convert into meters
                    way_first = Point()
                    way_first.x = result['WaypointX']/100
                    way_first.y = result['WaypointY']/100
                    way_first.z = result['MissionAltitude']/100

                    # Update the waypoint element with the current time
                    arrived_at_waypoint_sql = 'UPDATE Waypoint SET WaypointTimeArrived = NOW() WHERE WaypointID = ' + result['WaypointID'] + ';'
                    self.cursor.execute(arrived_at_waypoint_sql)

                    # Take off and wait 5 sec.
                    drone_control_object.takeoff()
                    time.sleep(5)
                    drone_control_object.stop()
                    continue
                else:
                    # Grab waypoints (which are in cm) and convert into meters
                    way_second = Point()
                    way_second.x = result['WaypointX']/100
                    way_second.y = result['WaypointY']/100
                    way_second.z = result['MissionAltitude']/100

                    # Since we have two waypoints, initiate a move
                    drone_control_object.moveQuantum(way_first, way_second)

                    # Update the waypoint element with the current time
                    arrived_at_waypoint_sql = 'UPDATE Waypoint SET WaypointTimeArrived = NOW() WHERE WaypointID = ' + result['WaypointID'] + ';'
                    self.cursor.execute(arrived_at_waypoint_sql)

                    # We have moved to the second waypoint, so iterate to the next point
                    way_first = way_second
            # Mission is finished
            drone_control_object.land()
            complete_mission_sql = 'UPDATE Mission SET MissionStatus_MissionStatusID = 4 WHERE MissionID = ' + mission_id + ';'
            self.cursor.execute(complete_mission_sql)

        except (KeyboardInterrupt, SystemExit):
            drone_control_object.land()
            abort_mission_sql = 'UPDATE Mission SET MissionStatus_MissionStatusID = 3 WHERE MissionID = ' + mission_id + ';'
            self.cursor.execute(abort_mission_sql)
            raise
        except:
            drone_control_object.land()
            abort_mission_sql = 'UPDATE Mission SET MissionStatus_MissionStatusID = 3 WHERE MissionID = ' + mission_id + ';'
            self.cursor.execute(abort_mission_sql)
            print "Unexpected error:", sys.exc_info()[0]
