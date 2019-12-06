#!/home/rastech/catkin_ws/src/venv/bin/python
import rospy
import io
import os
import configparser

from google.cloud import speech
from STTRos import STTRos
from record import RecordWithoutSilence

config = configparser.ConfigParser()
config.read('/home/rastech/catkin_ws/src/config.ini')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get('KEY', 'google_cloud_key')

encoding = config.get('GOOGLE_SETTINGS', 'encoding')
sample_rate_hertz = int(config.get('GOOGLE_SETTINGS', 'sample_rate_hertz'))
language_code = config.get('GOOGLE_SETTINGS', 'language_code')

wave_file = 'recording.wav'
STT_text_file = 'STT.text'

print(os.getcwd())


def recognize_speech(filename):
    print("Contacting Google for Speech Recognition...")
    client = speech.SpeechClient()
    rec_config = speech.types.RecognitionConfig(
        encoding=encoding,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz
    )
    with io.open(filename, 'rb') as audio_file:
        response = client.recognize(
            config=rec_config,
            audio=speech.types.RecognitionAudio(content=audio_file.read())
        )
        for result in response.results:
            for alternative in result.alternatives:
                print('=' * 20)
                print('transcript: ' + alternative.transcript)
                print('confidence: ' + str(alternative.confidence))
    try:
        return response.results[0].alternatives[0].transcript
    except IndexError:  # the API key didn't work
        print("No internet connection")
        return " "
    except KeyError:  # the API key didn't work
        print("Invalid API key or quota maxed out")
    except LookupError:  # speech is unintelligible
        print("Could not understand audio")


def save_recognize_speech(wave, stt_text):
    print("save speech")
    text = open(stt_text, 'w')
    text.write(recognize_speech(wave))
    print("recognize end")
    text = open(stt_text, 'r')
    texts = text.readline()
    print(texts)
    text.close()
    return texts


def start():
    print('STT node start')
    while not rospy.is_shutdown():
        if ros.hotword_status:
            record.record_start(wave_file)
            texts = save_recognize_speech(wave_file, STT_text_file)
            ros.hotword_status = False
            ros.pub_stt.publish(texts)
    print('STT node stop')



if __name__ == "__main__":
    #ros
    ros = STTRos()
    rospy.init_node('STT', anonymous=True)
    rate = rospy.Rate(10)  # 10hz

    record = RecordWithoutSilence()

    try:
        start()
    except rospy.ROSInterruptException:
        pass