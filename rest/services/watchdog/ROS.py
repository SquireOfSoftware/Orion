from ardrone_msgs.msg import Navdata
import rospy
from std_msgs.msg import String
import time

class ROS:
        def __init__(self):
                self.last_seq = None

        def callback(self):
                rospy.loginfo(rospy.get_caller_id() + "data %s", Navdata)
                self.seq = data['header']['seq']
                return self.seq

        def listener():
                rospy.init_node('listener', anonymous=True)
                rospy.Subscriber("ardrone/navdata", Navdata, callback)
                # spin() simply keeps python from exiting until this node is stop$
                rospy.spin()

        def getLastSeq(self):
                return self.seq






