import unittest
import string
import random
import os
from Crypto.PublicKey import RSA
from unittest.case import SkipTest
from sneakers.encoders.rsa import Rsa

import sneakers
basePath = os.path.dirname(os.path.abspath(sneakers.__file__))

class TestRsa(unittest.TestCase):
    def setUp(self):
        self.randText = ''.join([random.choice(string.letters) for i in range(10)])

        pubPath = os.path.join(basePath, 'config', 'test_key.pub')
        privPath = os.path.join(basePath, 'config', 'test_key')

        if not os.path.isfile(pubPath) or not os.path.isfile(privPath):
            raise SkipTest('could not access RSA keypair in config folder')

        self.rsa = Rsa()

        # set some parameters
        for e in self.rsa.params['sending']:
            if e.name == 'publicKey':
                e.value = pubPath

        for e in self.rsa.params['receiving']:
            if e.name == 'privateKey':
                e.value = privPath

    def test_encode(self):
        encoded = self.rsa.encode(self.randText)
        decoded = self.rsa.decode(encoded)
        self.assertEqual(decoded, self.randText)
