from sneakers.modules import Channel


class File(Channel):
    requiredParams = {
        'sending': {
            'filename': 'Name of the file to write data to.'
        },
        'receiving': {
            'filename': 'Name of the file to read data from.'
        }
    }

    optionalParams = {
        'sending': {
            'mode': 'wa'
        },
        'receiving': {
            'mode': 'rb'
        }
    }

    maxLength = 10000000
    # 10 MB
    maxHourly = 10000

    def send(self, data):
        params = self.reqParams['sending']
        opt_params = self.optParams['sending']
        with open(params['filename'], opt_params['mode']) as f:
            f.write(data)
        return

    def receive(self):
        params = self.reqParams['receiving']
        opt_params = self.optParams['receiving']
        with open(params['filename'], opt_params['mode']) as f:
            data = f.read()
        return [data]
