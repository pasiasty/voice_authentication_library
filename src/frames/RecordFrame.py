__author__ = 'mpasek'

import wave
import pyaudio
import threading
import tkMessageBox
import os
from ttk import Progressbar

from src.frames.MyEntries import *
from src.frames.MyFrame import MyFrame
from src.processing.datadumper import DataDumper
from src.Constants import Constants

class RecordFrame(MyFrame):

    def __init__(self, parent):
        MyFrame.__init__(self, parent, 'Parametrize', (100,0))

        self.record_options = DataDumper.load_json_data(Constants.CONFIG_PATH)['record_options']
        self.record_time.set_value(self.record_options['duration'])
        self.thread = None

    def init_ui(self):
        MyFrame.init_ui(self)

        self.columnconfigure(0, weight=2, minsize=150)
        self.columnconfigure(1, weight=3, minsize=100)

        self.file_name      = TextEntry(self, 'Recorded file name')
        self.record_time    = TextEntry(self, 'Record time')
        self.progress_bar   = Progressbar(self, orient='horizontal', mode='determinate')

        self.progress_bar.grid(columnspan=2, sticky='NESW')

        Button(self, text='Record', command=self.threaded_record).grid(columnspan=2, sticky='NESW')

    def threaded_record(self):
        if self.thread == None or not self.thread.isAlive():
            self.thread = threading.Thread(target=self.record)
            self.thread.start()

    def record(self):

        frequency = int(self.record_options['frequency'])
        record_time = int(self.record_time.get_value())

        format = pyaudio.paInt16
        n_channels = 2
        chunk = 1024
        output_filename = Constants.RAW_FILES_PATH + self.file_name.get_value() + '.wav'

        splitted = self.file_name.get_value().split('/')
        if len(splitted) > 1:
            splitted = splitted[:-1]
            acc = Constants.RAW_FILES_PATH
            for el in splitted:
                acc += el + '/'
                if not os.path.isdir(acc):
                    os.mkdir(acc)

        audio = pyaudio.PyAudio()

        stream = audio.open(format=format, channels=n_channels,
                        rate=frequency, input=True,
                        frames_per_buffer=chunk)

        frames = []
        progress_step = 100. / int(frequency / chunk * record_time)


        for i in range(0, int(frequency / chunk * record_time)):
            data = stream.read(chunk)
            frames.append(data)
            self.progress_bar.step(progress_step)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(output_filename, 'wb')
        waveFile.setnchannels(n_channels)
        waveFile.setsampwidth(audio.get_sample_size(format))
        waveFile.setframerate(frequency)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        tkMessageBox.showinfo('Info', 'Finished recording')
        self.progress_bar.step(-100)