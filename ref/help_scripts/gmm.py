__author__ = 'mpasek'

from sklearn import mixture
import random
import numpy
import matplotlib.pyplot as plt

class GMM:

    def __init__(self):
        self.low_bound = 0
        self.high_bound = 100
        self.threshold = -15
        numpy.random.seed(1)
        random.seed(109)

    def randomize_point(self):
        return random.randrange(self.low_bound, self.high_bound), \
               random.randrange(self.low_bound, self.high_bound)

    def add_noise_to_point(self, (px, py), sigma = 1, num = 100):
        return [(px + sigma * numpy.random.randn(), py + sigma * numpy.random.randn()) for idx in range(num)]

    def plot_points(self, arr, filename):

        arr_x = [x for (x,_) in arr]
        arr_y = [y for (_,y) in arr]

        plt.figure()
        plt.plot(arr_x, arr_y, '.')
        plt.xlim(self.low_bound, self.high_bound)
        plt.ylim(self.low_bound, self.high_bound)
        plt.savefig('../images/{}.jpg'.format(filename))
        plt.close()

    def simple_plot(self, arr, filename):
        plt.figure()
        plt.plot(arr)
        plt.savefig('../images/{}.jpg'.format(filename))
        plt.close()

    def plot_multi_points(self, arrs, filename):

        plt.figure()

        for arr, c in arrs:
            arr_x = [x for (x,_) in arr]
            arr_y = [y for (_,y) in arr]
            plt.plot(arr_x, arr_y, '.' + c)

        plt.xlim(self.low_bound, self.high_bound)
        plt.ylim(self.low_bound, self.high_bound)
        plt.savefig('../images/{}.jpg'.format(filename))
        plt.close()

    def simple_multi_plot(self, arrs, filename):
        plt.figure()
        for i, arr in enumerate(arrs):
            plt.plot(arr, label='Class {}'.format(i+1))

        plt.legend(loc='lower right', shadow=True, fontsize='x-large')
        plt.savefig('../images/{}.jpg'.format(filename))
        plt.close()

    def prepare_random_data(self):

        data_1 = []
        data_2 = []
        sigmas = [3,3,3]
        mu_1 = []
        mu_2 = []

        for sigma in sigmas:
            mu_1.append(self.randomize_point())
            arr = self.add_noise_to_point(mu_1[-1], sigma)
            data_1 += arr

        for sigma in sigmas:
            mu_2.append(self.randomize_point())
            arr = self.add_noise_to_point(mu_2[-1], sigma)
            data_2 += arr

        return mu_1, mu_2, data_1, data_2

    def best_predict(self, g, sample):
        return g.predict_proba([sample])[0]

    def run(self):

        mu_1, mu_2, data_1, data_2 = self.prepare_random_data()

        g_1 = mixture.GMM(n_components=3)
        g_2 = mixture.GMM(n_components=3)

        g_1.fit(data_1)
        g_2.fit(data_2)

        assigned_1 = []
        assigned_2 = []
        unassigned = []

        points   = [self.randomize_point() for el in range(200)]
        scores_1 = g_1.score(points)
        scores_2 = g_2.score(points)

        for idx in range(len(points)):
            if scores_1[idx] > self.threshold:
                assigned_1.append(points[idx])
            elif scores_2[idx] > self.threshold:
                assigned_2.append(points[idx])
            else:
                unassigned.append(points[idx])

        self.simple_multi_plot([g_1.score(data_1), g_1.score(data_2)], 'gmm_score_comp')

        arr = [
            (data_1, 'b'),
            (assigned_1, 'c'),
            (data_2, 'r'),
            (assigned_2, 'm'),
            (unassigned, 'g')
        ]

        self.plot_multi_points(arr, 'gmm_classified')

        self.plot_points(data_1, 'gmm_raw_data_1')
        self.plot_points(data_2, 'gmm_raw_data_2')

if __name__ == '__main__':
    GMM().run()