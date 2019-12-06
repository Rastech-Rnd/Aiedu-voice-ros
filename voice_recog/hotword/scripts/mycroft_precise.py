#!/home/rastech/catkin_ws/src/venv/bin/python
import rospy
import time
import configparser

from precise_runner import PreciseEngine, PreciseRunner
from HotWordRos import HotWordRos

config = configparser.ConfigParser()
config.read('/home/rastech/catkin_ws/src/config.ini')

precise_engine = config.get('WAKE_WORD_SETTING', 'precise_engine')
wake_word_model = config.get('WAKE_WORD_SETTING', 'wake_word_model')

#
# def not_detected(x):
#     # global is_wake_up
#     # print(is_wake_up)
#     # print('not detected...')
#     print(x)
#     time.sleep(0.125)


def detectd():
    print('hotword detected!!!')
    ros.pub_hotword.publish(True)
    print('3 seconds pause')
    time.sleep(3)
    print('hotword detection restart')
    ros.pub_hotword.publish(False)


def start():
    print('hotword node start')
    while not rospy.is_shutdown():
        pass
    print('hotword node stop')


if __name__ == "__main__":
    #ros
    ros = HotWordRos()
    rospy.init_node('Hotword', anonymous=True)
    rate = rospy.Rate(10)  # 10hz

    # engine = PreciseEngine('/home/rastech/catkin_ws/src/venv/bin/precise-engine',
    #                        '/home/rastech/catkin_ws/src/fero_speaker/script/precise-data-models/new_ifero_191021.pb')
    engine = PreciseEngine(precise_engine, wake_word_model)

    runner = PreciseRunner(engine, sensitivity=0.5, on_activation=lambda: detectd())
    runner.start()

    try:
        start()
    except rospy.ROSInterruptException:
        pass