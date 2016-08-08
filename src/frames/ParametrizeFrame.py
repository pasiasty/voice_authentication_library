__author__ = 'mariusz'

import os
import threading
from Tkinter import *

from src.processing.datadumper import DataDumper
from src.processing.signalparametrizer import SignalParametrizer
from src.processing.waveprocessor import WaveProcessor
from src.frames.MyFrame import MyFrame
from src.Constants import Constants

class ParametrizeFrame(MyFrame):

    def __init__(self, parent):
        MyFrame.__init__(self, parent, 'Parametrize', (800,100))

        self.refresh_lists()
        self.thread = None

    def init_ui(self):
        MyFrame.init_ui(self)

        self.columnconfigure(0, weight=1, minsize=400)
        self.columnconfigure(1, weight=1, minsize=400)

        self.input_list = Listbox(self, width=0, selectmode='multiple')
        self.input_list.grid(row=0, column=0, sticky='NESW')

        self.output_list = Listbox(self, width=0)
        self.output_list.grid(row=0, column=1, sticky='NESW')

        Button(self, text='parametrize', width=0, command=self.parametrize).grid(columnspan=2, sticky='NESW')

        self.status_var = StringVar()
        Label(self, textvariable=self.status_var, anchor=W, width=0).grid(columnspan=2, sticky='NESW')
        self.status_var.set('idle')

    def refresh_lists(self):

        self.input_list.delete(0, END)

        files = []

        root = Constants.RAW_FILES_PATH
        for r,d,f in os.walk(root):
            for file in f:
                files.append(os.path.join(r[len(root):],file).split('.')[0])

        files.sort()

        for file in files:
            self.input_list.insert(END, file)

        self.output_list.delete(0, END)

        files = []

        root =Constants.PARAMETRIZED_PATH
        for r,d,f in os.walk(root):
            for file in f:
                files.append(os.path.join(r[len(root):],file).split('.')[0])

        files.sort()

        for file in files:
            self.output_list.insert(END, file)

    def parametrize(self):

        DataDumper.init_plot_dumping('', Constants.PARAMETRIZATION_PROCESS)
        config = DataDumper.load_json_data(Constants.CONFIG_PATH)

        parametrizer = SignalParametrizer(config['parametrization_properties'],
                                          config['dump_options'],
                                          self.status_var)

        selections = [self.input_list.get(el) for el in self.input_list.curselection()]

        if self.thread == None or not self.thread.isAlive():
            self.thread = threading.Thread(target=self.parametrize_selected_files, args=(parametrizer, selections))
            self.thread.start()

    def parametrize_wav_file(self, parametrizer, filename):
        input_path = Constants.RAW_FILES_PATH
        output_path = Constants.PARAMETRIZED_PATH

        if '/' in filename:
            ind = filename.rfind('/')
            path = filename[:ind]
            if not os.path.isdir(path):
                os.system('mkdir -p {}'.format(output_path + path))

        wave_processor = WaveProcessor(filename=input_path + filename + '.wav')

        self.status_var.set('{:40} extracting_wave_file'.format(filename))
        data = wave_processor.extract_raw_data()
        extracted = parametrizer.extract_mfcc(data, filename)

        DataDumper.store_json_data(extracted, output_path + filename + '.proc')

    def parametrize_selected_files(self, parametrizer, selections):

        for selection in selections:
            DataDumper.init_plot_dumping(selection.replace('/', '_'), Constants.PARAMETRIZATION_PROCESS)
            self.parametrize_wav_file(parametrizer, selection)
            self.refresh_lists()

        self.status_var.set('idle')