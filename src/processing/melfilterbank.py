__author__ = 'samsung'

import math

from src.processing.datadumper import DataDumper

class MelFilterBank:

    def __init__(self, parameters, frame_length, frequency, do_dump):
        num_coeff    = parameters['num_coeff'] + 2
        self.frame_length = frame_length

        freq_low, freq_high = parameters['freq_bounds']

        mel_low = self.freq_to_mel(freq_low)
        mel_high = self.freq_to_mel(freq_high)

        mel_step = (mel_high - mel_low) / float(num_coeff-1)
        mel_indices = [mel_low + i * mel_step for i in range (num_coeff)]
        freq_indices = [self.mel_to_freq(el) for el in mel_indices]
        self.indices = [int(ind / float(frequency) * (frame_length+1)) for ind in freq_indices]
        self.prepare_filter_data()

        if do_dump:
            DataDumper.dump_plot(self.filters, 'filter_bank', 'dim_2_plot_mult')


    def freq_to_mel(self, x):
        return 1125 * math.log(1 + x/700.)

    def mel_to_freq(self, x):
        return 700 * (math.exp(x/1125.) - 1)

    def prepare_filter_data(self):

        self.filters = []

        for m, act in enumerate(self.indices):
            filter = []

            if m==0 or m==(len(self.indices)-1):
                continue

            prev = self.indices[m-1]
            next = self.indices[m+1]

            for k in range(self.frame_length/2):
                if k < prev:
                    filter.append(0)
                if k >= prev and k <= act:
                    filter.append((k-prev)/float(act-prev))
                if k > act and k <= next:
                    filter.append((next-k)/float(next-act))
                if k > next:
                    filter.append(0)

            self.filters.append(filter)

    def filter_data(self, data):
        res = []

        for mel_filter in self.filters:
            arr = zip(mel_filter, data)
            res.append([mel_coeff * data_el
                        for (mel_coeff, data_el) in arr])

        return res