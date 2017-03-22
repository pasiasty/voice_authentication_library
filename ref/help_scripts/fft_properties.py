__author__ = 'mpasek'

import matplotlib.pyplot as plt
import math
from numpy.fft import fft
from decimal import Decimal
import random

def full_plot(x, filename):

    fig = plt.figure()
    t = plt.subplot2grid((2,2), (0,0), colspan=2)
    t.plot(x)
    t.set_title('Time domain')

    x = fft(x)
    epsilon = Decimal(10) ** -10
    re = [float(Decimal(el.real).quantize(epsilon)) for el in x]
    im = [float(Decimal(el.imag).quantize(epsilon)) for el in x]

    n = len(x) / 2

    re = re[n:] + re[:n]
    im = im[n:] + im[:n]

    ax1 = fig.add_subplot(223)
    ax1.stem(re)
    ax1.set_title('DFT Real part')
    ax2 = fig.add_subplot(224)
    ax2.stem(im)
    ax2.set_title('DFT Imag part')
    plt.tight_layout()
    plt.savefig('../images/{}.jpg'.format(filename))
    plt.close()

def cycle_shift(arr, n):
    return arr[n:] + arr[:n]

def mult_signals(x, y):
    return [el_x * el_y for (el_x, el_y) in zip(x, y)]

def gen_sine():
    return [math.sin(x * 2 * math.pi / 20) for x in range(100)]

def gen_rect():
    return [(x / 20) % 2 for x in range(100)]

def gen_sawtooth():
    return [x % 20 for x in range(100)]

def gen_rect_window():
    res = []
    width = 20
    n = 100

    for i in range(n):
        if i <= n/2 - (width/2) or i >= n/2 + (width/2):
            res.append(0)
        else:
            res.append(1)
    return res

def gen_hamming_window():
    alpha = 0.54
    beta  = 0.46
    N = 86

    return [alpha - beta * math.cos(2 * math.pi * n / (N - 1)) for n in range(N)]

def plot_filters_spectrum():

    plt.figure()
    x = [1] * 50 + [0] * 50
    t = plt.subplot(221)
    t.stem(x)
    t.set_title('Lowpass filter')

    x = [0] * 50 + [1] * 50
    t = plt.subplot(222)
    t.stem(x)
    t.set_title('Highpass filter')

    x = [0] * 25 + [1] * 50 + [0] * 25
    t = plt.subplot(223)
    t.stem(x)
    t.set_title('Bandpass filter')

    x = [1] * 25 + [0] * 50 + [1] * 25
    t = plt.subplot(224)
    t.stem(x)
    t.set_title('Bandstop filter')

    plt.tight_layout()
    plt.savefig('../images/{}.jpg'.format('filters_spectrum'))
    plt.close()

def plot_sinc_func():

    x = [-18 + 0.01 * i for i in range(3601)]
    ind = [-1800 + i for i in range(3601)]
    x[1800] = 1
    sinx = [math.sin(el) for el in x]
    zipped = zip(x, sinx)
    sincx = [val / arg for (arg, val) in zipped]
    sincx[1800] = 1

    plt.figure()
    plt.plot(ind, sincx)
    plt.tight_layout()
    plt.savefig('../images/{}.jpg'.format('sinc'))
    plt.close()

def dual_plot(before, after, filename):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(before)
    ax1.set_title('before {}'.format(filename))
    ax2 = fig.add_subplot(212)
    ax2.set_title('after {}'.format(filename))
    ax2.plot(after)
    plt.tight_layout()
    plt.savefig('../images/{}.jpg'.format(filename))
    plt.close()

def preemphase(signal):
    res = []
    for ind, el in enumerate(signal[1:]):
        res.append(-signal[ind] * 0.97 + el)

    return res

def mfcc_steps():

    signal = [random.randrange(-100,100,1) for i in range(100)]
    sine = [math.sin(x * 2 * math.pi / 100) for x in range(100)]
    signal = zip(sine, signal)
    signal = [sig_el / 1000. + sine_el for sine_el, sig_el in signal]
    dual_plot(signal, preemphase(signal), 'MFCC_preemphase')

    signal = [1125 * math.log(1 + x/700.) for x in range(1,8000)]

    plt.figure()
    plt.plot(signal)
    plt.xlabel('Linear frequency [Hz]')
    plt.ylabel('Mel frequency')
    plt.tight_layout()
    plt.savefig('../images/{}.jpg'.format('MFCC_mel_to_linear'))
    plt.close()

def main():

    sine = gen_sine()
    rect = gen_rect()
    saw  = gen_sawtooth()
    rect_window = gen_rect_window()
    hamming = gen_hamming_window()

    full_plot(sine, 'sine')
    full_plot(saw, 'saw')
    full_plot(rect_window, 'rect_window')
    full_plot(hamming, 'hamming')

    m_sine_rect = mult_signals(sine, rect_window)
    full_plot(m_sine_rect, 'm_sine_rect')

    sh_sine = cycle_shift(sine, 13)
    full_plot(sh_sine, 'sine_shifted')

    sub_sine = sine[:86]
    h_sub_sine = mult_signals(hamming, sub_sine)
    full_plot(sub_sine, 'sub_sine')
    full_plot(h_sub_sine, 'h_sub_sine')

    plot_filters_spectrum()
    plot_sinc_func()

    mfcc_steps()

if __name__ == '__main__':
    main()