#!/usr/bin/python2

__author__ = 'mpasek'

import unittest
import os
import sys

arr = os.getcwd().split(os.sep)
path = os.sep.join(arr[:len(arr)-1])
sys.path.append(path)

from src.processing.waveprocessor import WaveProcessor
from src.processing.u2decoder import U2Decoder
from src.processing.signalparametrizer import SignalParametrizer
from src.processing.datadumper import DataDumper


class U2ProcessorTests(unittest.TestCase):

    def test_merge(self):
        arr = [chr(1), chr(5)]
        res = U2Decoder.merge_bytes(arr)

        self.assertEqual(res, '0000000100000101')

    def test_inverse(self):
        arg = '0000100110011'
        res = U2Decoder.inverse(arg)

        self.assertEqual(res, '1111011001100')

    def test_increment(self):
        arg = '010101'
        res = U2Decoder.increment(arg)
        self.assertEqual(res, '0010110')

    def test_is_negative(self):
        neg = '10010101101'
        pos = '01101010110'

        self.assertTrue(U2Decoder.is_negative(neg))
        self.assertFalse(U2Decoder.is_negative(pos))

    def test_decode_u2(self):
        arg = [chr(237)]
        res = U2Decoder.decode_u2(arg)

        self.assertAlmostEqual(res, -19/65536.)

class WavProcessorTests(unittest.TestCase):

    def test_open_wav_file(self):

        wave_processor = WaveProcessor(filename='../unit_tests_data' + os.sep + 'test.wav')
        serialized = str(wave_processor)
        data = wave_processor.extract_raw_data()

        expected_serialized = '''../unit_tests_data''' + os.sep + '''test.wav

Num channels:                       2
Sample width:                       2
Frame rate:                     48000
Frames count:                   49650
Compression name:      not compressed
Compression type:                NONE
'''

        self.assertEqual(serialized, expected_serialized)
        self.assertEqual(len(data), 49650)

class SignalParametrizerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        parameters = SignalParametrizer.default_processing_parameters()
        parameters['decimation_factor'] = 5
        cls.parametrizer = SignalParametrizer(parameters,
                                              SignalParametrizer.dump_none_parameters())

    def test_decimate(self):

        data = [1,2,3,4,5,6,7,8,9,10]
        exp_res = [1,6]

        res = self.parametrizer.decimate(data)

        self.assertEqual(res, exp_res)

    def test_divide_into_frames(self):

        data = range(0,800)
        exp_res = [range(beg*88, beg*88+220) for beg in range(7)]
        res = self.parametrizer.divide_into_frames(data)

        self.assertEqual(res, exp_res)

    def test_zero_pad(self):
        data = [1,1,1,1,1]
        exp_res = [0,1,1,1,1,1,0,0]
        res = self.parametrizer.zero_pad(data)

        self.assertEqual(res, exp_res)

class MelFilterBankTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        parameters = SignalParametrizer.default_processing_parameters()
        parameters['mel_params']['freq_bounds'] = (300, 4000)
        parameters['mel_params']['num_coeff'] = 12
        cls.processor = SignalParametrizer(parameters,
                                           SignalParametrizer.dump_none_parameters())
        cls.bank = cls.processor.mel_filter_bank

    def test_mel_freq_transform(self):
        x = 36.47
        res = self.bank.mel_to_freq(self.bank.freq_to_mel(x))

        self.assertAlmostEqual(x, res)

class DataDumperTests(unittest.TestCase):

    def test_write_and_load(self):

        filename = '../unit_tests_data' + os.sep + 'dump.txt'
        data = [{
            'asa' : 123,
            'ggw' : 'ble'
        }, 'bgd', 45]

        dumper = DataDumper()
        dumper.store_json_data(data, filename)
        res = dumper.load_json_data(filename)

        self.assertEqual(res, data)

if __name__ == '__main__':

    test_cases = [
        U2ProcessorTests,
        WavProcessorTests,
        SignalParametrizerTests,
        MelFilterBankTests,
        DataDumperTests
    ]

    for test_case in test_cases:

        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        res = unittest.TextTestRunner(verbosity=2).run(suite)






