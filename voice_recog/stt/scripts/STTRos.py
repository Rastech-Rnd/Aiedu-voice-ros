import rospy
from std_msgs.msg import *


class STTRos:

    def __init__(self):
        self.pub_stt = rospy.Publisher('/aiedu/stt/result', String, queue_size=10)
        self.sub_hotword = rospy.Subscriber('/aiedu/hotword/result', Bool, self.hotword_detected_callback)
        self.hotword_status = False

    def hotword_detected_callback(self, is_detectd):
        self.hotword_status = is_detectd.data