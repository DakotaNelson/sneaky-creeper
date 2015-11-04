from sneakers.modules import Channel

class File(Channel):

    description = """\
        Reads or writes data to or from a file with the specified name. Useful for testing and out of band transfer.
    """

    requiredParams = {
        'sending': {
            'filename': 'Name of the file to write data to.'
        },
        'receiving': {
            'filename': 'Name of the file to read data from.'
        }
    }

    maxLength = 10000000
    # 10 MB
    maxHourly = 10000

    def send(self, data):
        params = self.params['sending']
        with open(params['filename'], 'wa') as f:
            f.write(data)
        return

    def receive(self):
        params = self.params['receiving']
        with open(params['filename'], 'rb') as f:
            data = f.read()
        return [data]
