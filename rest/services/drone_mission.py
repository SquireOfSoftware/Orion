import roslib
import rospy
import json
import time

from database_access_layer import Connector
from drone_control import *
from resource_locator import resource

class drone_mission(Connector, resource):
    def __init__(self):
        self.controller = drone_control()
        super(self).__init__()
        pass

    def start(self):
        return

