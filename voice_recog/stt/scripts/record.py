#!/home/rastech/catkin_ws/src/venv/bin/python3
import subprocess
import pyaudio
import wave
from sys import byteorder
from array import array, ArrayType
from struct import pack
import math
import audioop
import time
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import math
import contextlib



class RecordWithoutSilence:
    def __init__(self):
        self.timesout = 10
        self.timeout_start = 0
        self.threshold = 1000
        # self.threshold_silence = 3000
        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        self.rate = 16000
        self.wait_time = 30
        self.silent_wait = 130
        self.is_it_silence = False
        self.channel = 1
        # self.fname = '/home/rastech/catkin_ws/src/fero_speaker/script/recent.wav'
        # self.outname = '/home/rastech/catkin_ws/src/fero_speaker/script/recent_convert.wav'
        self.cutOffFrequency = 1500.0
        self.input_device_index = 17

    def running_mean(self, x, windowSize):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

    # from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
    def interpret_wav(self, raw_bytes, n_frames, n_channels, sample_width, interleaved=True):

        if sample_width == 1:
            dtype = np.uint8  # unsigned char
        elif sample_width == 2:
            dtype = np.int16  # signed 2-byte short
        else:
            raise ValueError("Only supports 8 and 16 bit audio formats.")

        channels = np.fromstring(raw_bytes, dtype=dtype)

        if interleaved:
            # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
            channels.shape = (n_frames, n_channels)
            channels = channels.T
        else:
            # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
            channels.shape = (n_channels, n_frames)

        return channels


    def audio_int(self, num_samples=50):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the 20% largest intensities recorded.
        """

        print("Getting intensity values from mic.")
        p = pyaudio.PyAudio()

        stream = p.open(format=self.format,
                        channels=self.channel,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk_size)
                        # input_device_index=self.input_device_index)

        values = [math.sqrt(abs(audioop.avg(stream.read(self.chunk_size), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print(" Finished ")
        print(" Average audio intensity is ", r)
        stream.close()
        p.terminate()
        return r

    def record_start(self, wave_file):
        print("please speak a word into the microphone")
        # self.record_to_file(path + '.wav')
        self.record_to_file(wave_file)
        print("done - result written to", wave_file)

        # with contextlib.closing(wave.open(self.fname, 'rb')) as spf:
        #     sampleRate = spf.getframerate()
        #     ampWidth = spf.getsampwidth()
        #     nChannels = spf.getnchannels()
        #     nFrames = spf.getnframes()
        #
        #     # Extract Raw Audio from multi-channel Wav File
        #     signal = spf.readframes(nFrames * nChannels)
        #     spf.close()
        #     channels = self.interpret_wav(signal, nFrames, nChannels, ampWidth, True)
        #
        #     # get window size
        #     # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
        #     freqRatio = (self.cutOffFrequency / sampleRate)
        #     N = int(math.sqrt(0.196196 + freqRatio ** 2) / freqRatio)
        #
        #     # Use moviung average (only on first channel)
        #     filtered = self.running_mean(channels[0], N).astype(channels.dtype)
        #
        #     wav_file = wave.open(wave_file, "w")
        #     wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        #     wav_file.writeframes(filtered.tobytes('C'))
        #     wav_file.close()

    def record_to_file(self, path):
        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = self.record()
        data = pack('<' + ('h' * len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(self.channel)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(data)
        wf.close()

    def record(self):
        """
        Record a word or words from the microphone and
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the
        start and end, and pads with 0.5 seconds of
        blank sound to make sure VLC et al can play
        it without getting chopped off.
        """

        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=self.channel, rate=self.rate,
                        input=True, output=True,
                        frames_per_buffer=self.chunk_size)
                        # input_device_index=self.input_device_index)

        num_silent = 0
        snd_started = False

        r = array('h')
        cnt = 0
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + self.timesout:
            # little endian, signed short
            snd_data = array('h', stream.read(self.chunk_size))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self.is_silent(snd_data)
            print(cnt, ",", num_silent, ",", max(snd_data), ",", silent)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True
                num_silent = 0
            elif not silent and snd_started:
                num_silent = 0
            if silent and not snd_started:
                num_silent += 1
                if num_silent > self.silent_wait:
                    self.is_it_silence = True
                    break
            if snd_started and num_silent > self.wait_time:
                self.is_it_silence = False
                break

        sample_width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.normalize(r)
        # r = self.trim(r)
        r = self.add_silence(r, 0.1)
        return sample_width, r

    def is_silent(self, snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.threshold

    def normalize(self, snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')  # type: ArrayType
        for i in snd_data:
            r.append(int(i * times))
        return r

    def trim(self, snd_data):
        "Trim the blank spots at the start and end"

        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > self.threshold:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in range(int(seconds * self.rate))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds * self.rate))])
        return r

    def find_device_id(self, device_name):
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        print(p.get_default_input_device_info())

        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if device_name in p.get_device_info_by_host_api_device_index(0, i).get('name'):
                    print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
                    print(i)
                    print('find success')

                    # return i
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        return None

if __name__ == "__main__":

    # subprocess.call(["amixer", "-D", "(hw:2,0)", "sset", "Mic", "65%"])
    # print(time.time())
    # subprocess.call(["amixer", "-c", "0", "sset", "Mic",Samson Meteor "65%"])
    record = RecordWithoutSilence()
    record.input_device_index = record.find_device_id('Samson Meteor')
    record.threshold = record.audio_int()
    print('threshold : %d' % record.threshold)
    record.record_start('recent')
