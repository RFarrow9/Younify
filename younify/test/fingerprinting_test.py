from younify import *

log = motley.setup_logger(__name__)


class TestFingerprintingMethods(unittest.TestCase):
    def test_instantiation(self):
        fingerprint = fingerprinter.FingerPrinter()
        print(fingerprint)


if __name__ == '__main__':
    unittest.main()
