import unittest
import string
import base64
import random

from sneakers.encoders.b64 import B64

class TestB64(unittest.TestCase):
    def setUp(self):
        self.randText = ''.join([random.choice(string.letters) for i in range(10)])
        self.b64 = B64()

    def test_encode(self):
        encoded = self.b64.encode(self.randText)

        self.assertEqual(encoded, base64.b64encode(self.randText))

    def test_decode(self):
        encoded = base64.b64encode(self.randText)
        decoded = self.b64.decode(encoded)

        self.assertEqual(decoded, self.randText)
