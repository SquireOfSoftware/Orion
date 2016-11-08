from database_access_layer import connector

class Recover():
	def __init__(self):
		pass
		
	def startROS(self):		
		if isDroneAvailable(self):		
			SPAWN ROS
			SPAWN sputnik

	def isDroneAvailable(self):
		self.droneObject = Drone(self)
		return (self.droneObject.retreive(self))	
		
