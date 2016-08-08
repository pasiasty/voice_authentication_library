__author__ = 'mpasek'

import os
import threading
from Tkinter import *

from src.frames.MyFrame import MyFrame
from src.processing.classifier import Classifier
from src.Constants import Constants
from src.processing.datadumper import DataDumper

class AdjustModelFrame(MyFrame):

    def __init__(self, parent):
        MyFrame.__init__(self, parent, 'Adjust model', (400,100))

        self.fill_list()
        config = DataDumper.load_json_data(Constants.CONFIG_PATH)

        self.dump_options       = config['dump_options']
        self.detect_properties  = config['detecting_properties']
        self.thread             = None

    def init_ui(self):
        MyFrame.init_ui(self)

        self.file_list = Listbox(self)
        self.file_list.pack(fill=X)

        Button(self, text='Go', command=self.adjust_model_job).pack(fill=X)

        self.status_var = StringVar()
        Label(self, textvariable=self.status_var, anchor=W).pack(fill=X)
        self.status_var.set('idle')

    def adjust_model_job(self):
        if self.thread == None or not self.thread.isAlive():
            self.thread = threading.Thread(target=self.adjust_model)
            self.thread.start()

    def adjust_model(self):

        self.status_var.set('merging data')

        selection = self.file_list.get(self.file_list.curselection()[0])
        DataDumper.init_plot_dumping(selection, 'ADJ')

        clfs = {}

        for sample_name in Constants.LEARNING_FILES:

            data = list(DataDumper.load_json_data(Constants.PARAMETRIZED_PATH +
                                             selection +
                                             '/' + sample_name + '.proc'))

            if self.dump_options['dumps_enabled']:
                DataDumper.dump_plot(data, 'adjust_input', 'dim_3_plot')

            clfs[sample_name] = Classifier(self.detect_properties, self.dump_options, sample_name, self.status_var)
            clfs[sample_name].fit(data)
            clfs[sample_name].store_to_file()

        self.status_var.set('idle')

    def fill_list(self):
        self.file_list.delete(0, END)
        files = [el.split('.')[0] for el in os.listdir(Constants.PARAMETRIZED_PATH)
                 if os.path.isdir(Constants.PARAMETRIZED_PATH + el)]
        files.sort()

        for file in files:
            self.file_list.insert(END, file)

    def merge_selected_data(self):

        selections = [self.file_list.get(el) for el in self.file_list.curselection()]
        data = []
        curr_file = '_'.join(selections)

        for selection in selections:

            data += list(DataDumper.load_json_data(Constants.PARAMETRIZED_PATH + selection + '.proc'))

        return (data, curr_file)