
from database_access_layer import connector
class Drone:
        def __init__(self):
                self.testConnector = connector()
                self.testConnector.connect()
                self.testCursor = self.testConnector.cursor


        def retreive(self):
                self.value = "SELECT DroneStatus_DroneStatusID from Drone;"
                self.testCursor.execute(self.value)
                self.newValue = 0
                for (DroneStatus_DroneStatusID) in self.testCursor:
                        self.newValue += ("{}".format(DroneStatus_DroneStatusID[0]))
                return (self.newValue==1)
		
		
