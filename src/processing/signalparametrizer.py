import sys
import math
from numpy.fft import fft
from scipy.fftpack import dct
from decimal import Decimal

from src.processing.datadumper import DataDumper
from src.processing.melfilterbank import MelFilterBank


class SignalParametrizer:

    @classmethod
    def default_processing_parameters(cls):
        parameters = {}

        parameters['mel_params'] = {}
        parameters['mel_params']['freq_bounds']   = (15, 4000) # [Hz]
        parameters['mel_params']['num_coeff']     = 26
        parameters['filter_coeff']                = 0.97
        parameters['input_freq']                  = 44100      # [Hz]
        parameters['decimation_factor']           = 5
        parameters['frame_length']                = 25         # [ms]
        parameters['frame_step']                  = 10         # [ms]
        parameters['delta_depth']                 = 2

        parameters['steps'] = {
                        'perform_windowing'       : True,
                        'append_deltas'           : True,
                        'perform_feature_warping' : True,
                        'mean_subtraction'        : True
                    },

        return parameters

    @classmethod
    def dump_none_parameters(cls):
        parameteres = {
        'selected_frame'            : 0,
        'dumps_enabled'             : False
        }

        return parameteres

    @classmethod
    def dump_all_parameters(cls):
        parameteres = {
        'selected_frame'            : 83,
        'dumps_enabled'             : True
        }

        return parameteres

    def __init__(self, parameters, dump_options, log_callback=None):

        self.filter_coeff      = parameters['filter_coeff']
        self.input_freq        = parameters['input_freq']
        self.decimation_factor = parameters['decimation_factor']
        self.frame_length      = parameters['frame_length']
        self.frame_step        = parameters['frame_step']
        self.delta_depth       = parameters['delta_depth']
        self.steps             = parameters['steps']

        self.log_callback      = log_callback
        self.dump_options      = dump_options

        self.mel_filter_bank = \
            MelFilterBank(parameters['mel_params'],
                          self.estimate_frame_length(),
                          self.input_freq / self.decimation_factor,
                          self.dump_options['dumps_enabled'])

    def extract_mfcc(self, data, filename):

        if self.dump_options['dumps_enabled']:
            DataDumper.dump_plot(data,
                                 'original_signal',
                                 'dim_2_plot')

        if self.log_callback is not None:
            self.log_callback.set('{:40} pre_emphase'
                                  .format(filename))
        data = self.pre_emphase(data)

        if self.dump_options['dumps_enabled']:
            DataDumper.dump_plot(data,
                                 'preemphased_signal',
                                 'dim_2_plot')

        if self.log_callback is not None:
            self.log_callback.set('{:40} decimate'
                                  .format(filename))
        data = self.decimate(data)

        if self.log_callback is not None:
            self.log_callback.set('{:40} divide_into_frames'
                                  .format(filename))
        frames = self.divide_into_frames(data)

        res = []

        for ind, frame in enumerate(frames):

            if self.log_callback is not None:
                self.log_callback.set('{:40} processing {} of {} frames'
                                      .format(filename, ind+1, len(frames)))
            frame = self.zero_pad(frame)

            if self.dump_options['dumps_enabled'] and ind == \
                    self.dump_options['selected_frame']:
                DataDumper.dump_plot(frame,
                                     'padded_signal',
                                     'dim_2_plot')

            if self.steps['perform_windowing']:
                frame = self.apply_windowing(frame)

            if self.dump_options['dumps_enabled'] and ind == \
                    self.dump_options['selected_frame']:
                DataDumper.dump_plot(frame,
                                     'windowed_signal',
                                     'dim_2_plot')

            frame = self.apply_fft(frame)

            if self.dump_options['dumps_enabled'] and ind == \
                    self.dump_options['selected_frame']:
                DataDumper.dump_plot(frame,
                                     'after_fft_signal',
                                     'dim_2_plot')

            mel_filter_results = self.mel_filter_bank.filter_data(frame)
            vector = []

            if self.dump_options['dumps_enabled'] and ind == \
                    self.dump_options['selected_frame']:
                DataDumper.dump_plot(mel_filter_results,
                                     'mel_filtered_signal',
                                     'dim_3_plot')

            for mel_filter_result in mel_filter_results:
                power = self.calculate_signal_power(mel_filter_result)
                vector.append(math.log(power))

            if self.dump_options['dumps_enabled'] and ind == \
                    self.dump_options['selected_frame']:
                DataDumper.dump_plot(vector,
                                     'mel_power_signal',
                                     'dim_2_rect')

            vector = self.discrete_cosine_transform(vector)

            if self.dump_options['dumps_enabled'] and ind == \
                    self.dump_options['selected_frame']:
                DataDumper.dump_plot(vector,
                                     'cosine_transformed_signal',
                                     'dim_2_rect')

            vector = self.liftering(vector)

            if self.dump_options['dumps_enabled'] and ind == \
                    self.dump_options['selected_frame']:
                DataDumper.dump_plot(vector,
                                     'liftered_signal',
                                     'dim_2_rect')

            res.append(vector)

        if self.dump_options['dumps_enabled']:
            DataDumper.dump_plot(res,
                                 'parametrized_raw',
                                 'dim_3_plot')

        if self.steps['append_deltas']:
            if self.log_callback is not None:
                self.log_callback.set('{:40} appending deltas'
                                      .format(filename))
            res = self.append_deltas_and_deltasdeltas(res)

            if self.dump_options['dumps_enabled']:
                DataDumper.dump_plot(res,
                                     'parametrized_with_delta',
                                     'dim_3_plot')

        if self.steps['perform_feature_warping']:
            if self.log_callback is not None:
                self.log_callback.set('{:40} feature warping'
                                      .format(filename))

            res = self.feature_warp(res, filename)
            if self.dump_options['dumps_enabled']:
                DataDumper.dump_plot(res,
                                     'feature_warped',
                                     'dim_3_plot')

        if self.steps['mean_subtraction']:
            if self.log_callback is not None:
                self.log_callback.set('{:40} cepstral mean subtraction'
                                      .format(filename))

            res = self.cepstral_mean_subtraction(res)
            if self.dump_options['dumps_enabled']:
                DataDumper.dump_plot(res, 'cepstral_mean_subtraction',
                                     'dim_3_plot')

        return res

    def estimate_frame_length(self):
        freq = self.input_freq / self.decimation_factor
        dt = 1./freq
        frame_len  = int(math.floor(self.frame_length / (dt * 1000)))
        power = 1

        while power < frame_len:
            power *= 2

        return power

    def pre_emphase(self, data):
        result = []

        for ind, el in enumerate(data[1:]):
            result.append(el - self.filter_coeff * data[ind-1])

        return result

    def decimate(self, data):
        return data[::self.decimation_factor]

    def divide_into_frames(self, data):
        freq = self.input_freq / self.decimation_factor
        dt = 1./freq
        frame_len  = int(math.floor(self.frame_length / (dt * 1000)))
        frame_step = int(math.floor(self.frame_step   / (dt * 1000)))

        ind = 0
        res = []

        while (ind + frame_len) < len(data):
            res.append(data[ind:ind+frame_len])
            ind += frame_step

        return res

    def zero_pad(self, frame):
        power = 1

        while power < len(frame):
            power *= 2

        diff = power - len(frame)
        left = int(math.floor(diff/2))
        right = diff - left

        left_pad  = [0 for i in range(left)]
        right_pad = [0 for i in range(right)]

        return left_pad + frame + right_pad

    def apply_windowing(self, frame):
        res = []
        N = len(frame)

        for n, el in enumerate(frame):
            coeff = 0.53836 - 0.46164 * math.cos(2 * math.pi * n / (N-1))
            res.append(coeff * el)

        return res

    def apply_fft(self, frame):
        res = fft(frame)
        return res[:len(res)/2]

    def calculate_signal_power(self, mel_filter_result):

        res = sys.float_info.epsilon

        for el in mel_filter_result:
            res += abs(el)**2

        res /= len(mel_filter_result)
        return res ** 0.5

    def discrete_cosine_transform(self, vector):
        return dct(vector)

    def liftering(self, vector):
        return vector[1:13]

    def cepstral_mean_subtraction(self, arg):
        num_coeffs = len(arg[0])
        means = []

        for i in range(num_coeffs):
            res = 0
            for el in arg:
                res += el[i]
            means.append(res / len(arg))

        for vector in arg:
            for i in range(num_coeffs):
                vector[i] -= means[i]

        return arg

    def append_deltas_and_deltasdeltas(self, arg):

        divider = 2. * sum(n**2 for n in range(self.delta_depth))

        res = []

        for t in range(self.delta_depth, len(arg)-self.delta_depth):
            vector = [0 for i in range(len(arg[0]))]

            for n in range(self.delta_depth):
                for k in range(len(arg[0])):
                    val = n * (arg[t+n][k] - arg[t-n][k]) / divider
                    vector[k] += val

            res.append(list(arg[t]) + list(vector))

        return res

    def feature_warp(self, arg, filename=None):

        epsilon = Decimal(10) ** -2

        def warp_single_row(signal):

            def get_histogram(arr):
                max_arr = max(arr)
                min_arr = min(arr)

                histogram = [0] * (int((max_arr - min_arr) /
                                       float(epsilon))+1)

                for el in arr:
                    index = (int((el - min_arr) / float(epsilon)))
                    histogram[index] += 1

                return histogram

            def histogram_to_cdf(histogram):
                cdf = []
                for i in range(len(histogram)):
                    cdf.append(sum(histogram[:(i+1)]))

                all_samples = float(sum(histogram))
                cdf = [float(Decimal(el / all_samples)
                             .quantize(epsilon))
                       for el in cdf]

                return cdf

            def prepare_norm_cdf(sigma, mu):

                def normcdf(x, arg_mu, arg_sigma):

                    def erfcc(x):

                        z = abs(x)
                        t = 1. / (1. + 0.5*z)
                        r = t * math.exp(-z*z-1.26551223+
                                         t*(1.00002368+t*(.37409196+
                            t*(.09678418+t*(-.18628806+t*(.27886807+
                            t*(-1.13520398+t*(1.48851587+t*(-.82215223+
                            t*.17087277)))))))))
                        if (x >= 0.):
                            return r
                        else:
                            return 2. - r

                    t = x-arg_mu
                    y = 0.5*erfcc(-t/(arg_sigma*math.sqrt(2.0)))
                    if y>1.0:
                        y = 1.0
                    return float(Decimal(y).quantize(epsilon))

                return [0] + \
                       [normcdf(mu - 3*sigma +
                                float(epsilon) * idx, mu, sigma)
                              for idx in range(int(6 * sigma /
                                                   float(epsilon)))] + [1]

            def first_greater(arr, arg):
                for idx in range(len(arr)):
                    if arg <= arr[idx]:
                        return idx

                return len(arg)-1

            def translate_signal(signal, values):
                result = []

                for el in signal:
                    found = False
                    for (old, new) in values:
                        if (old - float(epsilon)) <= \
                                el <= \
                                (old + float(epsilon)):
                            result.append(new)
                            found = True
                            break

                    if not found:
                        result.append(el)

                return result

            max_sig = max(signal)
            min_sig = min(signal)

            sigma = (max_sig - min_sig) / 6.
            mu    = (min_sig + max_sig) / 2.

            sig_hist = get_histogram(signal)
            sig_cdf  = histogram_to_cdf(sig_hist)
            norm_cdf = prepare_norm_cdf(sigma, mu)

            indices = [first_greater(norm_cdf, el) for el in sig_cdf]
            values = [(min_sig + idx * float(epsilon), min_sig +
                       indices[idx] * float(epsilon))
                      for idx in range(len(indices))]
            return translate_signal(signal, values)

        num_coeffs  = len(arg[0])
        num_vectors = len(arg)

        res = []

        for idx in range(num_vectors):
            res.append([0] * num_coeffs)

        for idx in range(num_coeffs):

            if self.log_callback is not None:
                self.log_callback.set('{:40} warping {} of {} coefficients'
                                      .format(filename, idx+1, num_coeffs))

            row = [el[idx] for el in arg]
            row = warp_single_row(row)

            for row_idx, el in enumerate(row):
                res[row_idx][idx] = el

        return res
