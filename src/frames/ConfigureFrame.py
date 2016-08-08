__author__ = 'mariusz'

import os.path
import tkMessageBox

from src.processing.datadumper import DataDumper
from src.frames.MyEntries import *
from src.frames.MyFrame import MyFrame
from src.Constants import Constants

class ConfigureFrame(MyFrame):

    def __init__(self, parent):
        MyFrame.__init__(self, parent, 'Configure', (400,0))

        if os.path.isfile(Constants.CONFIG_PATH):
            self.dictionary_to_gui(DataDumper.load_json_data(Constants.CONFIG_PATH))

    def prepare_group(self, name):
        MyEntry.counter = 0
        group = LabelFrame(self, text=name, padx=5, pady=5)
        group.pack(padx=10, pady=10, fill=X)
        group.columnconfigure(0, weight=1)
        group.columnconfigure(1, weight=1)

        return group

    def init_ui(self):

        MyFrame.init_ui(self)

        group = self.prepare_group('Recording options')

        self.record_frequency = TextEntry(group, 'Record frequency [Hz]')
        self.record_duration  = TextEntry(group, 'Record duration [s]')

        group = self.prepare_group('Parametrization steps')

        self.perform_windowing       = CheckEntry(group, 'Perform windowing')
        self.append_deltas           = CheckEntry(group, 'Append deltas')
        self.perform_feature_warping = CheckEntry(group, 'Perform Feature Warping')
        self.mean_subtraction        = CheckEntry(group, 'Cepstral mean subtraction')

        group = self.prepare_group('Parametrization properties')

        self.mel_freq_min           = TextEntry(group, 'Mel min frequency [Hz]')
        self.mel_freq_max           = TextEntry(group, 'Mel max frequency [Hz]')
        self.mel_num_coeff          = TextEntry(group, 'Mel number of coefficients')
        self.pream_filter_coeff     = TextEntry(group, 'Preamble filter coeff')
        self.input_freq             = TextEntry(group, 'Input frequency [Hz]')
        self.decimation_factor      = TextEntry(group, 'Decimation factor')
        self.frame_length           = TextEntry(group, 'Frame length')
        self.frame_step             = TextEntry(group, 'Frame step')
        self.delta_depth            = TextEntry(group, 'Delta depth')

        group = self.prepare_group('Detecting properties')

        self.detect_PCA                   = CheckEntry(group,  'Principal Component Analysis')
        self.detect_GMM                   = CheckEntry(group,  'Gaussian Mixtures')

        group = self.prepare_group('Dumping options')

        self.frame_number_to_dump           = TextEntry(group, 'Frame number to dump')
        self.dumps_enabled                  = CheckEntry(group,  'Dumps enabled')
        self.debug_prints                   = CheckEntry(group,  'Debug prints enabled')

        bottom_panel = Frame(self)
        bottom_panel.pack(fill=X)
        bottom_panel.columnconfigure(0, weight=5)
        bottom_panel.columnconfigure(1, weight=4)
        Button(bottom_panel, text='OK', width=0, command=self.ok_button_click).grid(column=0, row=0, sticky='NESW')
        Button(bottom_panel, text='Cancel', width=0, command=self.cancel_button_click).grid(column=1, row=0, sticky='NESW')

    def gui_to_dictionary(self):
        try:
            res = {
                'record_options' : {
                    'frequency' : self.record_frequency.get_value(),
                    'duration'  : self.record_duration.get_value()
                },

                'parametrization_properties' : {
                    'steps' : {
                        'perform_windowing'       : self.perform_windowing.get_value(),
                        'append_deltas'           : self.append_deltas.get_value(),
                        'perform_feature_warping' : self.perform_feature_warping.get_value(),
                        'mean_subtraction'         : self.mean_subtraction.get_value(),
                    },

                    'mel_params' : {
                        'freq_bounds' : (int(self.mel_freq_min.get_value()), int(self.mel_freq_max.get_value())),
                        'num_coeff'   : int(self.mel_num_coeff.get_value())

                    },

                    'filter_coeff'      : float(self.pream_filter_coeff.get_value()),
                    'input_freq'        : int(self.input_freq.get_value()),
                    'decimation_factor' : int(self.decimation_factor.get_value()),
                    'frame_length'      : int(self.frame_length.get_value()),
                    'frame_step'        : int(self.frame_step.get_value()),
                    'delta_depth'       : int(self.delta_depth.get_value()),
                },

                'detecting_properties' : {
                    'PCA'       : bool(self.detect_PCA.get_value()),
                    'GMM'       : bool(self.detect_GMM.get_value()),
                },

                'dump_options' : {
                    'selected_frame'            : int(self.frame_number_to_dump.get_value()),
                    'dumps_enabled'             : bool(self.dumps_enabled.get_value()),
                    'debug_prints'              : bool(self.debug_prints.get_value()),
                }
            }
        except ValueError:
            tkMessageBox.showerror('Error', 'wrong input format')
            return None

        return res

    def dictionary_to_gui(self, dict):

        self.record_frequency   .set_value(dict['record_options']['frequency'])
        self.record_duration    .set_value(dict['record_options']['duration'])

        self.perform_windowing      .set_value(dict['parametrization_properties']['steps']['perform_windowing'])
        self.append_deltas          .set_value(dict['parametrization_properties']['steps']['append_deltas'])
        self.perform_feature_warping.set_value(dict['parametrization_properties']['steps']['perform_feature_warping'])
        self.mean_subtraction       .set_value(dict['parametrization_properties']['steps']['mean_subtraction'])

        self.mel_freq_min       .set_value(dict['parametrization_properties']['mel_params']['freq_bounds'][0])
        self.mel_freq_max       .set_value(dict['parametrization_properties']['mel_params']['freq_bounds'][1])
        self.mel_num_coeff      .set_value(dict['parametrization_properties']['mel_params']['num_coeff'])

        self.pream_filter_coeff .set_value(dict['parametrization_properties']['filter_coeff'])
        self.input_freq         .set_value(dict['parametrization_properties']['input_freq'])
        self.decimation_factor  .set_value(dict['parametrization_properties']['decimation_factor'])
        self.frame_length       .set_value(dict['parametrization_properties']['frame_length'])
        self.frame_step         .set_value(dict['parametrization_properties']['frame_step'])
        self.delta_depth        .set_value(dict['parametrization_properties']['delta_depth'])

        self.detect_PCA         .set_value(dict['detecting_properties']['PCA'])
        self.detect_GMM         .set_value(dict['detecting_properties']['GMM'])

        self.frame_number_to_dump           .set_value(dict['dump_options']['selected_frame'])
        self.dumps_enabled                  .set_value(dict['dump_options']['dumps_enabled'])
        self.debug_prints                   .set_value(dict['dump_options']['debug_prints'])

    def ok_button_click(self):
        dict = self.gui_to_dictionary()
        DataDumper.store_json_data(dict, Constants.CONFIG_PATH)
        self.close_window()

    def cancel_button_click(self):
        self.close_window()



