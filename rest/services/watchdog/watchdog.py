from database_access_layer import connector
#from mission_reader import mission_reader
import time	
class Watchdog:
	def __init__(self):
		self.recoverObject = Recover(self)
		self.abortObject = Abort(self)	
		self.rosObject = ROS(self)
		self.testConnector = connector()
        self.testCursor = self.testConnector.cursor		
				
	def watchDogProcess(self, seq):
		if compareSeq(self.seq):
			self.abortObject.killROS()
			self.recoverObject.startROS()			
			
	def compareSeq(self, seq):
		self.beforeSleepSeq = self.seq
		time.sleep(0.5)
		self.current = self.rosObject.getLastSeq(self)	
		return (self.current == self.seq)
	
	def main(self):
		self.rosObject.listener()
		self.rosObject.lastSeq = self.rosObject.callback()
		self.testConnector.connect()
		self.value = "select MetadataState, Drone_DroneID from Metadata"\
					 "where Drone_DroneID = (select Drone_DroneID from Mission where MissionStatus_MissionStatusID = 2)"\
					 "order by MetadataTimestamp desc limit 1;"
        self.testCursor.execute(self.value)
		self.newValue = 0
		for (MetadataState) in self.testCursor:
			self.newValue += ("{}".format(MetadataState[0]))	      

		while (self.newValue == 1 || self.newValue == 3 ||self.newValue == 4 ||self.newValue == 6 ||self.newValue == 7 ||self.newValue == 8 ||self.newValue == 9):
			watchDogProcess(self.lastSeq)		
		
if __name__ == "__main__":
		watchdog().main()


	
