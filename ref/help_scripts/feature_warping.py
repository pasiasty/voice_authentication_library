import matplotlib.pyplot as plt
import math
from decimal import Decimal
import random
import numpy as np

class FeatureWarping:

    def __init__(self):
        self.epsilon = Decimal(10) ** -2

    def apply_noise(self, arr):
        return [self.round(el + random.randrange(-100,100) / 50.) for el in arr]

    def sine_signal(self):
        sine = [math.sin(x * 2 * math.pi / 1000) for x in range(1000)]
        signal = [float(Decimal(el).quantize(self.epsilon)) for el in sine]
        return signal

    def rectangle_noise_signal(self):
        return [self.round(random.randrange(-100,100) / 50.) for el in range(50)]

    def normal_noise_signal(self):
        return np.random.normal(2, 1, 100)

    def round(self, arg):
        return float(Decimal(arg).quantize(self.epsilon))

    def get_histogram(self, arr):
        max_arr = max(arr)
        min_arr = min(arr)

        histogram = [0] * (int((max_arr - min_arr) / float(self.epsilon))+1)

        for el in arr:
            index = (int((el - min_arr) / float(self.epsilon)))
            histogram[index] += 1

        return histogram

    def histogram_to_cdf(self, histogram):
        cdf = []
        for i in range(len(histogram)):
            cdf.append(sum(histogram[:(i+1)]))

        all_samples = float(sum(histogram))
        cdf = [float(Decimal(el / all_samples).quantize(self.epsilon)) for el in cdf]

        return cdf

    def normcdf(self, x, arg_mu, arg_sigma):

        def erfcc(x):
            """Complementary error function."""
            z = abs(x)
            t = 1. / (1. + 0.5*z)
            r = t * math.exp(-z*z-1.26551223+t*(1.00002368+t*(.37409196+
                t*(.09678418+t*(-.18628806+t*(.27886807+
                t*(-1.13520398+t*(1.48851587+t*(-.82215223+
                t*.17087277)))))))))
            if (x >= 0.):
                return r
            else:
                return 2. - r

        t = x-arg_mu;
        y = 0.5*erfcc(-t/(arg_sigma*math.sqrt(2.0)));
        if y>1.0:
            y = 1.0;
        return float(Decimal(y).quantize(self.epsilon))

    def prepare_norm_cdf(self, sigma, mu):
        return [0] + [self.normcdf(mu - 3*sigma + float(self.epsilon) * idx, mu, sigma)
                      for idx in range(int(6 * sigma / float(self.epsilon)))] + [1]

    def translate_signal(self, signal, values):
        result = []

        for el in signal:
            found = False
            for (old, new) in values:
                if (old - float(self.epsilon)) <= el <= (old + float(self.epsilon)):
                    result.append(new)
                    found = True
                    break

            if not found:
                result.append(el)

        return result

    def simple_plot(self, arr, filename, type='normal'):
        plt.figure()
        if type == 'normal':
            plt.plot(arr)
        elif type == 'stem':
            plt.stem(arr)
        plt.savefig('../images/{}.jpg'.format(filename))
        plt.close()

    def plot_featuring_summary(self, orig_sig, feat_orig_sig, noised_sig, feat_noised_sig):

        fig = plt.figure()

        ax = fig.add_subplot(221)
        ax.plot(orig_sig)
        ax.set_title('Original signal')

        ax = fig.add_subplot(222)
        ax.plot(feat_orig_sig)
        ax.set_title('Featured original signal')

        ax = fig.add_subplot(223)
        ax.plot(noised_sig)
        ax.set_title('Noised signal')

        ax = fig.add_subplot(224)
        ax.plot(feat_noised_sig)
        ax.set_title('Featured noised signal')

        plt.tight_layout()
        plt.savefig('../images/{}.jpg'.format('feature_warping_summary'))
        plt.close()

    def first_greater(self, arr, arg):

        for idx in range(len(arr)):
            if arg <= arr[idx]:
                return idx

        return len(arg)-1

    def run(self):

        signal = self.rectangle_noise_signal()
        original_signal = signal
        noised_signal   = self.apply_noise(signal)

        max_sig = max(noised_signal)
        min_sig = min(noised_signal)

        min_orig_sig = min(original_signal)

        sigma = (max_sig - min_sig) / 6.
        mu    = (min_sig + max_sig) / 2.

        print 'Processing signal'

        orig_sig_hist   = self.get_histogram(original_signal)
        orig_sig_cdf    = self.histogram_to_cdf(orig_sig_hist)

        noised_sig_hist = self.get_histogram(noised_signal)
        noised_sig_cdf  = self.histogram_to_cdf(noised_sig_hist)

        print 'Preparing normal cdf'

        norm_cdf = self.prepare_norm_cdf(sigma, mu)

        print 'Translating noised signal'

        indices = [self.first_greater(norm_cdf, el) for el in noised_sig_cdf]
        values = [(min_sig + idx * float(self.epsilon), min_sig + indices[idx] * float(self.epsilon)) for idx in range(len(indices))]
        featured_noised_signal = self.translate_signal(noised_signal, values)

        print 'Translating original signal'

        indices = [self.first_greater(norm_cdf, el) for el in orig_sig_cdf]
        values = [(min_orig_sig + idx * float(self.epsilon), min_orig_sig + indices[idx] * float(self.epsilon)) for idx in range(len(indices))]
        featured_orig_signal = self.translate_signal(noised_signal, values)

        print 'Processing translated signal'

        featured_hist = self.get_histogram(featured_noised_signal)
        featured_cdf = self.histogram_to_cdf(featured_hist)

        print 'Storing plots'

        self.plot_featuring_summary(original_signal, featured_orig_signal,
                                    noised_signal, featured_noised_signal)

        self.simple_plot(noised_sig_cdf,           'feature_warping_noised_cdf')
        self.simple_plot(featured_cdf,             'feature_warping_featured_cdf')
        self.simple_plot(norm_cdf,                 'feature_warping_norm_cdf')

    def warp_feature(self, signal):

        max_sig = max(signal)
        min_sig = min(signal)

        sigma = (max_sig - min_sig) / 6.
        mu    = (min_sig + max_sig) / 2.

        sig_hist = self.get_histogram(signal)
        sig_cdf  = self.histogram_to_cdf(sig_hist)
        norm_cdf = self.prepare_norm_cdf(sigma, mu)

        indices = [self.first_greater(norm_cdf, el) for el in sig_cdf]
        values = [(min_sig + idx * float(self.epsilon), min_sig + indices[idx] * float(self.epsilon)) for idx in range(len(indices))]
        return self.translate_signal(signal, values)

if __name__ == '__main__':
    FeatureWarping().run()