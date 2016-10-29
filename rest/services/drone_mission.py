import roslib
import rospy
import json
import time

from database_access_layer import connector
from drone_control import *
from resource_locator import resource

class drone_mission(connector, resource):
    def __init__(self, resource_locator):
        connector.__init__(self)
        resource.__init__(self)

    def start(self):
        #Check if mission is running
        self.connect()
        #Execute check if any mission running for safety.
        sql = ""
        for result in self.cursor.execute(sql):
            if result.rowcount is 0
                return false
        #Query to get mission. Get all waypoints
        #
        sql = ""
        way_first = None
        for result in self.cursor.execute(sql):
            if way_first is None:
                way_first = result['x'], result['y']
                continue
            else:
                way_second = result['x'], result['y']
                #way point execute method
                way_first = way_second
            

