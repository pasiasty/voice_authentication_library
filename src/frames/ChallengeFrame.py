__author__ = 'mpasek'

import os
import threading
import tkMessageBox
from Tkinter import *

from src.frames.MyFrame import MyFrame
from src.processing.datadumper import DataDumper
from src.processing.classifier import Classifier
from src.Constants import Constants

class ChallengeFrame(MyFrame):

    def __init__(self, parent):
        MyFrame.__init__(self, parent, 'Challenge', (400,100))

        self.fill_list()
        self.dump_options   = DataDumper.load_json_data(Constants.CONFIG_PATH)['dump_options']
        self.detect_options = DataDumper.load_json_data(Constants.CONFIG_PATH)['detecting_properties']
        self.thread = None

    def init_ui(self):
        MyFrame.init_ui(self)

        self.file_list = Listbox(self, selectmode='multiple')
        self.file_list.pack(fill=X)

        Button(self, text='Go', command=self.challenge_job).pack(fill=X)

        self.status_var = StringVar()
        Label(self, textvariable=self.status_var, anchor=W).pack(fill=X)
        self.status_var.set('idle')

    def challenge_job(self):
        if self.thread == None or not self.thread.isAlive():
            self.thread = threading.Thread(target=self.challenge)
            self.thread.start()

    def challenge(self):

        selections = [self.file_list.get(el) for el in self.file_list.curselection()]

        err = 0

        for sample_name in Constants.LEARNING_FILES:

            DataDumper.init_plot_dumping(' '.join(selections) + '_' + sample_name, 'CHL')
            clf = Classifier(self.detect_options, self.dump_options, sample_name, self.status_var)
            clf.load_from_data()

            datas = []

            for curr_file in selections:
                datas.append(DataDumper.load_json_data(Constants.PARAMETRIZED_PATH + curr_file + '.proc'))

            clf.decision(datas, selections)

        tkMessageBox.showinfo('Info', 'Challenging finished')

    def fill_list(self):
        self.file_list.delete(0, END)
        files = [el.split('.')[0] for el in os.listdir(Constants.PARAMETRIZED_PATH)
                 if not os.path.isdir(Constants.PARAMETRIZED_PATH + el)]
        files.sort()

        for file in files:
            self.file_list.insert(END, file)
