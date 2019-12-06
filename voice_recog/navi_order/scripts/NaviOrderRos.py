import rospy
from std_msgs.msg import *
from move_base_msgs.msg import *


class NaviOrderRos:

    def __init__(self):
        self.pub_navi_order = rospy.Publisher('/move_base/result', MoveBaseActionResult, queue_size=10)
        self.sub_tts = rospy.Subscriber('/aiedu/tts/result', Bool, self.tts_callback)
        self.sub_chatbots_intent = rospy.Subscriber('/aiedu/chatbots/intent/result', String, self.intent_callback)
        self.intent_result = ''
        self.tts_result = False
        # self.header = std_msgs.msg.Header()
        # self.goalstatus = actionlib_msgs.msgs.GoalStatus()
        self.move_base = move_base_msgs.msg.MoveBaseActionResult()

    def intent_callback(self, intent):
        self.intent_result = intent.data

    def tts_callback(self, tts):
        self.tts_result = tts.data