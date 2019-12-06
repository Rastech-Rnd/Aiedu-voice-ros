import rospy
from std_msgs.msg import *


class ChatBotsRos:

    def __init__(self):
        self.pub_chatbots_responses = rospy.Publisher('/aiedu/chatbots/responses/result', String, queue_size=10)
        self.pub_chatbots_intent = rospy.Publisher('/aiedu/chatbots/intent/result', String, queue_size=10)
        self.sub_stt = rospy.Subscriber('/aiedu/stt/result', String, self.stt_callback)
        self.stt_result = ''

    def stt_callback(self, stt):
        self.stt_result = stt.data