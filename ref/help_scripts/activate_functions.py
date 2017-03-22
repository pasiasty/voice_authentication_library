__author__ = 'mpasek'

import matplotlib.pyplot as plt
import math


def threshold_func(x):
    if x <= 2:
        return -1
    return 1


def piecewise_linear(x):
    if x <= -1:
        return -1
    if x >= 1:
        return 1
    return x


def atan(x):
    return math.atan(x) / math.pi * 2


def simple_plot(args, arr, filename):
        plt.figure()
        plt.plot(args, arr)
        plt.ylim(-3,3)
        plt.savefig('../images/{}.jpg'.format(filename))
        plt.close()


if __name__ == '__main__':
    args = [idx / 1000. for idx in range(-8000,8000)]

    arr = [threshold_func(el) for el in args]
    simple_plot(args, arr, 'act_func_threshold')

    arr = [piecewise_linear(el) for el in args]
    simple_plot(args, arr, 'act_func_piecewise_lin')

    arr = [atan(el) for el in args]
    simple_plot(args, arr, 'act_func_atan')