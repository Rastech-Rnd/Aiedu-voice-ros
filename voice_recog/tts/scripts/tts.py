#!/home/rastech/catkin_ws/src/venv/bin/python
import rospy
import time
import os
import subprocess
import configparser

from google.cloud import texttospeech
from TTSRos import TTSRos

config = configparser.ConfigParser()
config.read('/home/rastech/catkin_ws/src/config.ini')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get('KEY', 'google_cloud_key')

language_code = config.get('GOOGLE_SETTINGS', 'language_code')
voice_type = config.get('GOOGLE_SETTINGS', 'voice_type')


def text_to_speech(text, filename):
    print("Contacting Google for Text-to-Speech...")
    tts_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(
        text=text
    )
    voice_params = texttospeech.types.VoiceSelectionParams(
        language_code=language_code,
        name=voice_type
    )
    audio_config = texttospeech.types.AudioConfig(audio_encoding='LINEAR16')
    response = tts_client.synthesize_speech(synthesis_input, voice_params, audio_config)

    with open(filename, 'wb') as f:
        f.write(response.audio_content)


def play_tts(text):
    text_to_speech(text, 'temp_tts.wav')
    play_audio('temp_tts.wav')


def play_audio(filename):
    print("Playing audio...")
    subprocess.call(["aplay", filename])


def start():
    print('TTS node start')
    while not rospy.is_shutdown():
        if ros.chatbots_responses != '':
            play_tts(ros.chatbots_responses)
            ros.chatbots_responses = ''
            ros.pub_tts.publish(True)
            print('move activate')
            time.sleep(3)
            print('3 seconds pause')
            ros.pub_tts.publish(False)
            print('TTS restart')
    print('TTS node stop')



if __name__ == "__main__":
    #ros
    ros = TTSRos()
    rospy.init_node('TTS', anonymous=True)
    rate = rospy.Rate(10)  # 10hz

    try:
        start()
    except rospy.ROSInterruptException:
        pass