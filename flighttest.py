#!usr/bin/env python

#DOES NOT FUCKING WORK

from rest.services.drone_control import *
from time import sleep

a = drone_control()


a.drone_takeoff()
sleep(1)
a.drone_land()
