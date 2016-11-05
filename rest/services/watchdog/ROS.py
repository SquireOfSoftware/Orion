
import time
from ardrone_msgs.msg import Navdata
import rospy
from std_msgs.msg import String
from database_access_layer import connector

class ROS:
	def __init__(self):
		self.last_seq = None

	def callback(self):
		rospy.loginfo(rospy.get_caller_id() + "I heard %s", Navdata)
		self.seq = data['header']['seq']    
		return self.seq
	
	def listener():  
		rospy.init_node('listener', anonymous=True)	  
		rospy.Subscriber("ardrone/navdata", Navdata, callback)  
		# spin() simply keeps python from exiting until this node is stopped
		rospy.spin()
  
	def getLastSeq(self):	
		return self.seq	
