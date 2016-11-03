import subprocess
import os, signal
import time
from database_access_layer import connector
class Abort:

	def killROS():
		process1 = subprocess.Popen("killROS.sh", shell = True)
		print 'process1 = ', process1.pid
		updateAbortStatus()
	
	def updateAbortStatus(self):
		self.save() 

