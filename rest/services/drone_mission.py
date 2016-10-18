import roslib
import rospy
import json
import time

from database_access_layer import connector
from drone_control import *
from resource_locator import resource

class drone_mission(connector, resource):
    def __init__(self,resource_locator):

        self.controller = drone_control()
        super(self).__init__()
        pass

    def start(self):
        return

