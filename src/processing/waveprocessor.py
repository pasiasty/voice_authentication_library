__author__ = 'mpasek'

import wave

from src.processing.u2decoder import U2Decoder


class WaveProcessor(object):

    def __init__(self, filename):
        self.name = filename
        self.file = wave.open(filename, 'rb')

    def __str__(self):
        res = ''
        res += self.name + '\n\n'

        res += 'Num channels:{:24}\n'.format(self.file.getnchannels())
        res += 'Sample width:{:24}\n'.format(self.file.getsampwidth())
        res += 'Frame rate:{:26}\n'.format(self.file.getframerate())
        res += 'Frames count:{:24}\n'.format(self.file.getnframes())
        res += 'Compression name:{}\n'.format(self.file.getcompname().rjust(20))
        res += 'Compression type:{}\n'.format(self.file.getcomptype().rjust(20))

        return res

    def extract_raw_data(self):

        res = []

        for i in range(self.file.getnframes()):
            frame = self.file.readframes(1)
            frame = frame[:len(frame)/self.file.getnchannels()]
            frame = frame[::-1]

            val = U2Decoder.decode_u2(list(frame))
            res.append(val)

        return res


