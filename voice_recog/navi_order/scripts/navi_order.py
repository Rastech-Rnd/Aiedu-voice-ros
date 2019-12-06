#!/home/rastech/catkin_ws/src/venv/bin/python
import rospy
import os
import configparser

import dialogflow_v2 as dialogflow
from NaviOrderRos import NaviOrderRos



def start():
    print('navi order start')
    while not rospy.is_shutdown():
        if ros.intent_result != '' and ros.tts_result == True:
            if ros.intent_result == 'Go to 01':
                ros.move_base.status.status = 11
                ros.pub_navi_order.publish(ros.move_base)
            elif ros.intent_result == 'Go to 02':
                ros.move_base.status.status = 12
                ros.pub_navi_order.publish(ros.move_base)
            elif ros.intent_result == 'Go to 03':
                ros.move_base.status.status = 13
                ros.pub_navi_order.publish(ros.move_base)
            else:
                pass
            ros.intent_result = ''
            ros.tts_result = False
    print('navi order stop')



if __name__ == "__main__":
    #ros
    ros = NaviOrderRos()
    rospy.init_node('navi_order', anonymous=True)
    rate = rospy.Rate(10)  # 10hz

    try:
        start()
    except rospy.ROSInterruptException:
        pass
