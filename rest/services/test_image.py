import rospy
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_writer:
    def __init__(self):
        rospy.init_node('test_image_writer', anonymous=True)
        self.image_sub = rospy.Subscriber("ardrone/image_raw", Image, self.image_callback)
        self.bridge = CvBridge()
        self.img_str = ""
        return

    def image_callback(self,data):
        try:
            self.cv2_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError, e:
            print(e)
        else:
            self.img_str = cv2.imencode('.png', self.cv2_img)
            

    def capture(self):
        cv2.imwrite('test.png', self.cv2_img)
