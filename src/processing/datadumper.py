__author__ = 'samsung'

import json, pickle
from pylab import *
import matplotlib.pyplot as plt
import numpy

from src.Constants import Constants

class DataDumper:

    curr_file  = ''

    counter    = 0

    @classmethod
    def init_plot_dumping(cls, curr_file, process):
        cls.counter = 0
        cls.curr_file = curr_file
        cls.process = process

    @classmethod
    def store_json_data(cls, data, filename):
        open(filename, 'w').write(json.dumps(data,
                                             sort_keys=True,
                                             indent=4,
                                             separators=(',', ': ')))

    @classmethod
    def load_json_data(cls, filename):
        return json.loads(open(filename, 'r').read())

    @classmethod
    def store_binary_data(cls, data, filename):
        open(filename, 'w').write(pickle.dumps(data))

    @classmethod
    def load_binary_data(cls, filename):
        return pickle.loads(open(filename, 'r').read())

    @classmethod
    def dump_plot(cls, data, stepname, mode, labels=None):

        dimensions = [str(len(data))]
        dim_2 = 0

        try:
            if len(data[0]) > 1:
                dimensions.append('x')
                dimensions.append(str(len(data[0])))
                dim_2 = len(data[0])
        except TypeError:
            pass

        dimensions = ' '.join(dimensions)

        if stepname == 'after_fft_signal':
            data = [abs(el) for el in data]

        if stepname == 'mel_filtered_signal':
            data = [[abs(el) for el in sub] for sub in data]

        if mode == 'dim_3_plot' and dim_2 == 2:
            mode = 'scatter_plot'

        plt.figure()
        plt.title(stepname + ' ' +  dimensions)

        if mode == 'dim_2_plot_mult':
            if labels is not None:
                zipped = zip(labels, data)
                for (label, el) in zipped:
                    plt.plot(el, label=label)

                plt.legend(loc='lower right', shadow=True, fontsize='x-large')
            else:
                for el in data:
                    plt.plot(el)

        if mode == 'dim_2_plot':
            plt.plot(data)

        if mode == 'stem_plot':
            plt.stem(data)

        if mode == 'dim_3_plot':

            map = plt.jet()
            new_data = []

            if len(data) < len(data[0]):
                data = numpy.transpose(data)

            scale = int(len(data) / len(data[0]))

            for sub in data:

                new_data.append(cls.repeat_element(sub, scale))

            data = new_data

            plt.imshow(numpy.transpose(data),map, interpolation='none')

        if mode == 'scatter_plot':

            X = [el[0] for el in data]
            Y = [el[1] for el in data]

            plt.scatter(X, Y)

        if mode == 'dim_2_rect':
            x = [i+1 for i in range(len(data))]
            plt.bar(x, data)

        if stepname != 'filter_bank':
            cls.counter += 1
            plt.savefig('{path}{filename}_{process}_{num:03d}_{stepname}.png'.format(
                    path=Constants.DUMPS_PATH,
                    filename=cls.curr_file,
                    process=cls.process,
                    num=cls.counter,
                    stepname=stepname))
        else:
            plt.savefig('{path}{process}_{stepname}.png'.format(
                    path=Constants.DUMPS_PATH,
                    process=cls.process,
                    stepname=stepname))

        plt.close()


    @classmethod
    def repeat_element(cls, list, n):
        res = []

        for el in list:
            for i in range(n):
                res.append(el)

        return res