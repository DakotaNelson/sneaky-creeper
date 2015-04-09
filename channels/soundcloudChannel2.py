import random
import struct
import wave


def send(data, params):
    SAMPLE_LEN = 50000

    frames = []

    for i in range(0, SAMPLE_LEN):
            value = random.randint(-32767, 32767)
            frames.append(struct.pack('h',value))

    wf = wave.open('output.wav', 'wb')
    wf.setnchannels(1)
    wf.setframerate(44100)
    wf.setsampwidth(2)
    wf.writeframes(b''.join(frames))
    wf.close()

    print "Done sending"
    return

def receive(params):
    pass


if __name__ == "__main__":
    send(1,1)
