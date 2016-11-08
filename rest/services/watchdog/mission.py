from database_access_layer import connector
class Mission:
	def __init__(self):
		self.testConnector = connector()
        self.testConnector.connect()
        self.testCursor = self.testConnector.cursor
	def save():
		self.value ="UPDATE Mission"\
					"SET MissionStatus_MissionStatusID =3"\
					"WHERE MissionStatus_MissionStatusID = 2"
		self.testCursor.execute(self.value)
		
