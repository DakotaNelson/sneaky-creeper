# Lendian stegonography system
import random

requiredParams = {
        'encode':{
            },
        'decode':{
            }
        }

def randomSound():
    return random.randint(-32767, 32767)

def encodeChar(char, encode_type='random'):
    # Turn into an integer
    char = ord(char)

    # Convert to bits with padding to ensure 8 bit
    bits = []
    for i in range(8):
        bits.append( char & 1 )
        char = char >> 1

    encoded_data = []
    if encode_type == 'random':
        for i in bits:
            tmp_data = randomSound()
            if i == 0:
                tmp_data = tmp_data & ~1
            else:
                tmp_data = tmp_data | 1

            encoded_data.append(str(tmp_data))

    else:
        #TODO: Is this how we are handling errors?
        print("No support for that encoding type yet!")
        exit()

    return encoded_data

def decodeChar(data_8bit):
    bits = []
    for i in data_8bit:
        bits.append( i & 1 )
    
    # Have to reverse bit set because of
    # how it was converted before
    bits = bits[::-1]
        
    # Convert to char
    char = 0
    for i in bits:
        char = char << 1
        if i == 0:
            char = char & ~1
        else:
            char = char | 1

    char = chr(char)
    return char

def encode(data, params=None):
    encoded_data = []
    for i in data:
        encoded_data += encodeChar(i)

    return encoded_data

def decode(data, params=None):
    data = data.split(',')
    bit_size = 8
    decoded_data = []

    # This division should NOT be a float division
    # in case encoding dataset that is bigger than
    # data size
    for i in range(len(data)/bit_size):
        singleChar = [int(i) for i in data[i*8:8+i*8]]
        decoded_data.append(decodeChar(singleChar))
    
    return ''.join(decoded_data)

if __name__ == "__main__":
    data_set = "Hello this is a large test of the de-stegranography system"
    encoded = encode(data_set);
    print(encoded)
    print(decode(encoded))
    
