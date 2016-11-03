


from resource_locator import resource, resource_locator
from database_access_layer import connector


class mission_reader(resource):
    def __init__(self, resource_locator):
        super(mission_reader, self).__init__(resource_locator)
        connector.__init__()

    def read(self):
        testConnector = connector()

        testConnector.connect()

        testQuery = "select MissionID, Drone_DroneID " \
                    "from Mission " \
                    "where MissionStatus_MissionStatusID = " \
                    "(select MissionStatusID " \
                    "from MissionStatus " \
                    "where MissionStatusName = 'IN PROGRESS');"
        testCursor = testConnector.cursor
        testCursor.execute(testQuery)

        for (MissionID, Drone_DroneID) in testCursor:
            print("{} {}".format(MissionID, Drone_DroneID))

        testConnector.disconnect()
