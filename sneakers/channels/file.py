from sneakers.modules import Channel, Parameter


class File(Channel):
    description = """\
        Reads or writes data to or from a file with the specified name. Useful for testing and out of band transfer.
        """

    params = {
        'sending': [
            Parameter('filename', True, 'Name of the file to write data to.'),
            Parameter('mode', False, 'Read mode for the sending file.', 'wa')
        ],
        'receiving': [
            Parameter('filename', True, 'Name of the file to read data from.'),
            Parameter('mode', False, 'Read mode for the receiving file.', 'rb')
        ]
    }

    maxLength = 10000000
    # 10 MB
    maxHourly = 10000

    def send(self, data):
        filename = self.param('sending', 'filename')
        mode = self.param('sending', 'mode')
        with open(filename, mode) as f:
            f.write(data)
        return

    def receive(self):
        filename = self.param('receiving', 'filename')
        mode = self.param('receiving', 'mode')
        with open(filename, mode) as f:
            data = f.read()
        return [data]
