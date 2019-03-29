from younify import fingerprinting
import unittest
import json

with open('c:\\config\\config.json') as f:
    config = json.load(f)

class TestFingerprintingMethods(unittest.TestCase):

    def test_instantiation(self):
        fingerprint = fingerprinting.fingerprinter()
        print(fingerprint)

if __name__ == '__main__':
    unittest.main()
