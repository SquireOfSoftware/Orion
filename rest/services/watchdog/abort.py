import subprocess
import os, signal
import time
class Abort:
	def __init__(self):
		
	def killROS(self):
		self.process1 = subprocess.Popen("killROS.sh", shell = True)
		print 'process1 = ', self.process1.pid
		updateAbortStatus(self)
	
	def updateAbortStatus(self):
		self.missObject = mission(self)
		self.missObject.save(self) 

		


