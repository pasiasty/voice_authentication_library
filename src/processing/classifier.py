from sklearn import mixture
from sklearn import decomposition
import numpy

from src.processing.datadumper import DataDumper
from src.Constants import Constants


class Algorithm(object):

    def __init__(self, log_callback, dump_options, letter):
        self.log_callback = log_callback
        self.dump_options = dump_options
        self.letter = letter

    def fit(self, data):
        pass

    def decision(self, data):
        pass

    def name(self):
        return ''

    def log_line(self, text):
        if self.log_callback != None:
            self.log_callback.set(self.letter +
                                  '_' + self.name() +
                                  '_' + text)


class GMM(Algorithm):

    def __init__(self, log_callback, dump_options, letter):
        Algorithm.__init__(self, log_callback, dump_options, letter)

    def fit(self, data):

        self.gmm = mixture.GMM(n_components=16)

        self.log_line('fitting GMM')

        self.gmm.fit(data)

        gmm_res = self.gmm.score(data)

        if self.dump_options['debug_prints']:
            print 'GMM ref score is:  {}'\
                .format(sum(gmm_res) / float(len(gmm_res)))

        if self.dump_options['dumps_enabled']:
            DataDumper.dump_plot(gmm_res, self.name() +
                                 '_decision_output',
                                 'dim_2_plot')

    def decision(self, data):

        gmm_res = self.gmm.score(data)

        if self.dump_options['dumps_enabled']:
            DataDumper.dump_plot(gmm_res, self.name() +
                                 '_decision_output',
                                 'dim_2_plot')

        if self.dump_options['debug_prints']:
            print 'GMM score is:  {}'\
                .format(sum(gmm_res) / float(len(gmm_res)))

        return gmm_res

    def name(self):
        return 'GMM'


class PCA(Algorithm):

    def __init__(self, log_callback, dump_options, letter):
        Algorithm.__init__(self, log_callback, dump_options, letter)

    def fit(self, data):

        self.pca = decomposition.ProbabilisticPCA(n_components=16)

        self.log_line('fitting PCA')

        self.pca.fit(numpy.asarray(data))

        pca_res = self.pca.score(numpy.asarray(data))

        if self.dump_options['debug_prints']:
            print 'PCA ref score is:  {}'\
                .format(sum(pca_res) / float(len(pca_res)))

        if self.dump_options['dumps_enabled']:
            DataDumper.dump_plot(pca_res, self.name() +
                                 '_decision_output',
                                 'dim_2_plot')

    def decision(self, data):

        pca_res = self.pca.score(numpy.asarray(data))

        if self.dump_options['dumps_enabled']:
            DataDumper.dump_plot(pca_res, self.name() +
                                 '_decision_output',
                                 'dim_2_plot')

        if self.dump_options['debug_prints']:
            print 'PCA score is:  {}'\
                .format(sum(pca_res) / float(len(pca_res)))

        return pca_res

    def name(self):
        return 'PCA'


class Classifier:

    def __init__(self,
                 detect_properties,
                 dump_options,
                 name,
                 log_callback = None):

        self.dump_options = dump_options
        self.log_callback = log_callback
        self.name = name

        self.algorithms = []

        if detect_properties['PCA']:
            self.algorithms.append(PCA(log_callback,
                                       dump_options,
                                       name))

        if detect_properties['GMM']:
            self.algorithms.append(GMM(log_callback,
                                       dump_options,
                                       name))

    def fit(self, data):

        for algorithm in self.algorithms:
            algorithm.fit(data)

        if self.log_callback is not None:
            self.log_callback.set('idle')

    def decision(self, datas, labels):

        min_len = min([len(el) for el in datas])
        datas = [el[:min_len] for el in datas]

        arr = zip(labels, datas)

        for algorithm in self.algorithms:
            decisions = []

            for label, data in arr:
                if self.dump_options['debug_prints']:
                    print 'processing {}'.format(label)
                decisions.append(algorithm.decision(data))
            DataDumper.dump_plot(decisions,
                                 'score of {}'.format(algorithm.name()),
                                                      'dim_2_plot_mult',
                                                      labels)

        if self.log_callback is not None:
            self.log_callback.set('idle')

    def store_to_file(self):

        for algorithm in self.algorithms:
            algorithm.log_callback = None

        DataDumper.store_binary_data(self.algorithms,
                              Constants.MODEL_PATH + '_' + self.name)

    def load_from_data(self):

        self.algorithms = \
            DataDumper.load_binary_data(Constants.MODEL_PATH + '_' + self.name)

        for algorithm in self.algorithms:
            algorithm.log_callback = self.log_callback