import rospy
from std_msgs.msg import *


class HotWordRos:

    def __init__(self):
        self.pub_hotword = rospy.Publisher('/aiedu/hotword/result', Bool, queue_size=10)

