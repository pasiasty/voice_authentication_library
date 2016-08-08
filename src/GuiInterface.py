#!/usr/bin/python2

__author__ = 'mariusz'

import sys
import os

arr = os.getcwd().split(os.sep)
path = os.sep.join(arr[:len(arr)-1])
sys.path.append(path)

import matplotlib
matplotlib.rcParams['agg.path.chunksize'] = 100000
matplotlib.use('Agg')

from Tkinter import *

from src.frames.ConfigureFrame import ConfigureFrame
from src.frames.ParametrizeFrame import ParametrizeFrame
from src.frames.RecordFrame import RecordFrame
from src.frames.AdjustModelFrame import AdjustModelFrame
from src.frames.ChallengeFrame import ChallengeFrame
from src.Constants import Constants

class GuiInterface(Frame):

    def __init__(self,):
        self.root = Tk()
        Frame.__init__(self, self.root)
        self.init_ui()

        if not os.path.isdir(Constants.PARAMETRIZED_PATH):
            os.mkdir(Constants.PARAMETRIZED_PATH)
        if not os.path.isdir(Constants.RAW_FILES_PATH):
            os.mkdir(Constants.RAW_FILES_PATH)
        if not os.path.isdir(Constants.DUMPS_PATH):
            os.mkdir(Constants.DUMPS_PATH)

    def init_ui(self):

        self.root.resizable(0,0)
        self.root.minsize(300,0)
        self.root.title("GUI Interface")
        self.pack(fill=X)

        button_args = {
            'fill'  : X,
            'ipadx' : 20,
            'ipady' : 7
        }

        self.configure_parametrization_button = Button(self, text='Configure', command=self.configure_paramertrization)
        self.configure_parametrization_button.pack(button_args)

        self.parametrize_data_button = Button(self, text='Parametrize data', command=self.parametrize)
        self.parametrize_data_button.pack(button_args)

        self.adjust_model_button = Button(self, text='Adjust model', command=self.adjust_model)
        self.adjust_model_button.pack(button_args)

        self.challenge_button = Button(self, text='Challenge', command=self.challenge)
        self.challenge_button.pack(button_args)

        self.record_sound_button = Button(self, text='Record sound', command=self.record)
        self.record_sound_button.pack(button_args)

    def run(self):
        self.root.mainloop()

    def configure_paramertrization(self):
        ConfigureFrame(self).run()

    def parametrize(self):
        ParametrizeFrame(self).run()

    def record(self):
        RecordFrame(self).run()

    def adjust_model(self):
        AdjustModelFrame(self)

    def challenge(self):
        ChallengeFrame(self)

if __name__ == '__main__':
    GuiInterface().run()