import roslib
import rospy
import json
import time

from database_access_layer import Connector
from drone_control import *

class drone_mission(Connector):
    def __init__(self):
        self.controller = drone_control()
        super(self).__init__()
        pass

    def start(self):
        return

