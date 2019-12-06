#!/home/rastech/catkin_ws/src/venv/bin/python
import rospy
import os
import configparser

import dialogflow_v2 as dialogflow
from ChatBotsRos import ChatBotsRos

config = configparser.ConfigParser()
config.read('/home/rastech/catkin_ws/src/config.ini')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get('KEY', 'dialogflow_key')

project_id = config.get('DIALOGFLOW_SETTINGS', 'project_id')
session_id = config.get('DIALOGFLOW_SETTINGS', 'session_id')
language_code = config.get('DIALOGFLOW_SETTINGS', 'language_code')


def detect_intent_texts(prj_id, ssn_id, texts, lngg_cod):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(prj_id, ssn_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=texts, language_code=lngg_cod)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))

    result_intent = format(
        response.query_result.intent.display_name)
    result_fulfillment_text = format(
        response.query_result.fulfillment_text)

    return result_intent, result_fulfillment_text


def start():
    print('dialog flow node start')
    while not rospy.is_shutdown():
        if ros.stt_result != '':
            intent, texts = detect_intent_texts(project_id, session_id, ros.stt_result, language_code)
            ros.stt_result = ''
            ros.pub_chatbots_responses.publish(texts)
            ros.pub_chatbots_intent.publish(intent)
    print('dialog flow node stop')



if __name__ == "__main__":
    #ros
    ros = ChatBotsRos()
    rospy.init_node('Chatbots', anonymous=True)
    rate = rospy.Rate(10)  # 10hz

    try:
        start()
    except rospy.ROSInterruptException:
        pass
