import unittest
import string
import random
import os
from Crypto.PublicKey import RSA
from sneakers.encoders.rsa import Rsa

class TestRsa(unittest.TestCase):
    def setUp(self):
        self.randText = ''.join([random.choice(string.letters) for i in range(10)])

        self.rsa = Rsa()
        self.rsa.params['encode']['publicKey'] = os.path.join(
          "test_encoders", "rsa_test_keys", "test_key.pub"
        )

        self.rsa.params['decode']['privateKey'] = os.path.join(
          "test_encoders", "rsa_test_keys", "test_key"
        )

    def test_encode(self):
        encoded = self.rsa.encode(self.randText)
        decoded = self.rsa.decode(encoded)
        self.assertEqual(decoded, self.randText)
