# Lendian stegonography system
# As of right now this can only encode the data
# into randomly generated integers.
from sneakers.modules import Encoder

import random

class Lendiansteganography(Encoder):

    description = """\
        Encodes data into the least significant two bits of randomly generated signed integers.
    """

    @staticmethod
    def __random_sound():
        return random.randint(-32767, 32767)

    def __encode_char(self, char, encode_type='random'):
        # Turn into an integer
        char = ord(char)

        # Convert to bits with padding to ensure 8 bit
        bits = []
        for i in range(8):
            bits.append(char & 1)
            char >>= 1

        encoded_data = []
        if encode_type == 'random':
            for i in bits:
                tmp_data = self.__random_sound()
                if i == 0:
                    tmp_data &= ~1
                else:
                    tmp_data |= 1

                encoded_data.append(str(tmp_data))
        else:
            raise NotImplementedError('Please choose a different encoding type')

        return encoded_data

    def set_params(self, p={}):
        return p

    @staticmethod
    def __decode_char(data_8bit):
        bits = []
        for i in data_8bit:
            bits.append(i & 1)

        # Have to reverse bit set because of
        # how it was converted before
        bits = bits[::-1]

        # Convert to char
        char = 0
        for i in bits:
            char <<= 1
            if i == 0:
                char &= ~1
            else:
                char |= 1

        char = chr(char)
        return char

    def encode(self, data):
        encoded_data = []
        for i in data:
            encoded_data += self.__encode_char(i)

        return encoded_data

    def decode(self, data):
        data = data.split(',')
        bit_size = 8
        decoded_data = []

        # This division should NOT be a float division
        # in case encoding dataset that is bigger than
        # data size
        for i in range(len(data) / bit_size):
            single_char = [int(i) for i in data[i * 8:8 + i * 8]]
            decoded_data.append(self.__decode_char(single_char))

        return ''.join(decoded_data)
