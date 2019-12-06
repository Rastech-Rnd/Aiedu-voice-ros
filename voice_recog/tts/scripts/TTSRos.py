import rospy
from std_msgs.msg import *


class TTSRos:

    def __init__(self):
        self.pub_tts = rospy.Publisher('/aiedu/tts/result', Bool, queue_size=10)
        self.sub_chatbots_responses = rospy.Subscriber\
            ('/aiedu/chatbots/responses/result', String, self.chatbots_responses_callback)
        self.sub_chatbots_intent = rospy.Subscriber\
            ('/aiedu/chatbots/intent/result', String, self.chatbots_intent_callback)
        self.chatbots_responses = ''
        self.chatbots_intent = ''

    def chatbots_responses_callback(self, responses):
        self.chatbots_responses = responses.data

    def chatbots_intent_callback(self, intent):
        self.chatbots_intent = intent.data