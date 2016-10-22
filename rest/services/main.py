#from resource_locator import resource_locator
#from drone_metadata import drone_metadata
#from drone_control import drone_control
#from drone_media import drone_media
from database_access_layer import connector
#from rest.management_constants import MISSION_STATUS


testConnector = connector()

testConnector.connect()

testQuery = "select MissionID, Drone_DroneID " \
            "from Mission " \
            "where MissionStatus_MissionStatustID = (select MissionStatusID " \
                                                    "from MissionStatus " \
                                                    "where MissionStatusName = 'QUEUED');"
testCursor = testConnector.cursor
testCursor.execute(testQuery)

for (MissionID, Drone_DroneID) in testCursor:
    print("{} {}".format(MissionID, Drone_DroneID))

testConnector.disconnect()
