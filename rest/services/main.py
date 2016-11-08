from resource_locator import resource_locator
from drone_metadata import drone_metadata
from drone_control import drone_control
from drone_mission import drone_mission
from drone_media import drone_media
from database_access_layer import connector
from mission_reader import mission_reader
import rospy
import logging
import time
import sys

sys.path.append('/opt/ros/kinetic/setup.sh')

logging.basicConfig(filename="/home/orion/orion-project/orion_project/main.log", level=logging.DEBUG)
mlog = logging.getLogger('main')

def tester():
    test = drone_control()
    time.sleep(10)
    test.test2()
    print("Test initialised i guess")

    return

def test_init():
    locator = resource_locator()
    drone_control(locator)
    drone_media(locator)
    drone_metadata(locator)
    drone_mission(locator)
    print("Initialisation Successful")
    return

def main():
    mlog.debug("Main Executed.")
    locator = resource_locator()
    drone_control(locator)
    drone_media(locator)
    drone_metadata(locator)
    drone_mission(locator)
    mlog.debug("Created Resources.")
    # rospy.init_node('orion_everything', anonymous=True)
    time.sleep(5)
    print("Initialisation Successful, calling drone mission")
    #locator.getDroneMission().start_test()  # NOTE this will call exit when done, just takes off, hovers and lands
    mlog.debug("Mission Ended")
    locator.getDroneMission().start()

if __name__ == "__main__":
    print("Attempting to run mission")
    main()
