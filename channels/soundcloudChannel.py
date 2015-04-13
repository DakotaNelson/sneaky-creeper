import random
import struct
import wave
import soundcloud
import os, re, urllib

client = soundcloud.Client(
    client_id=os.environ.get('SOUNDCLOUD_ID'),
    client_secret=os.environ.get('SOUNDCLOUD_Secret'),
    username=os.environ.get('SOUNDCLOUD_GMAIL'),
    password=os.environ.get('SOUNDCLOUD_PASS')
)

SONG_NAME = 'test'

def send(data, params):
    SAMPLE_LEN = 10000

    frames = []
    '''
    for i in range(0, SAMPLE_LEN):
            value = random.randint(-32767, 32767)
            frames.append(struct.pack('h',value))
    '''
    f = open('test.txt','r')
    for i in f:
        frames.append(i)

    wf = wave.open('output.wav', 'wb')
    wf.setnchannels(1)
    wf.setframerate(44100)
    wf.setsampwidth(2)
    wf.writeframes(b''.join(frames))
    wf.close()

    print "Done creating sound file"
    track = client.post('/tracks', track={
        'title': SONG_NAME,
        'sharing':'public',
        'asset_data': open('output.wav','rb'),
        'tag_list':'tag1 \"hip hop\"',
        'downloadable': True })
    print "Done uploading"

    os.remove('output.wav')
    return

def receive(params):
    #urllib.urlretrieve("http://soundcloud.com/user255215947/" +SONG_NAME+ "/download", 'file.wav')
    wf = wave.open('file.wav', 'r')
    print wf.getnframes()


    # TRYING TO OPEN IT AS A TXT FILE
    #f = open('file.wav','r')
    #for i in f.read():
    #    print struct.unpack('s', i)
    #struct.pack('c',f.read())
    
if __name__ == "__main__":
    #send(1,1)
    receive(1)
