from resource_locator import resource_locator
from drone_metadata import drone_metadata
from drone_control import drone_control
from drone_mission import drone_mission
from drone_media import drone_media
from database_access_layer import connector
from mission_reader import mission_reader
import time
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
    locator = resource_locator()
    drone_control(locator)
    drone_media(locator)
    drone_metadata(locator)
    drone_mission(locator)
    locator.getDroneMission().start()

if __name__ == "__main__":
    main()
