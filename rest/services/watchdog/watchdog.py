from database_access_layer import connector
#from mission_reader import mission_reader
import time	

class watchdog:
	def __init__(self):
		pass

	def watchDogProcess(self, seq):
		if compareSeq(self.seq):
			self.killROS()
			self.startROS()			
			
	def compareSeq(self, seq):
		self.beforeSleepSeq = seq
		time.sleep(0.5)
		current = getLastSeq()	
		return (current == seq)
	
	def main(self):
		self.listener()
		self.lastSeq = self.callback()
		while (true):
			watchDogProcess(lastSeq)		
		
	if __name__ = "__main__":
		main()


	


