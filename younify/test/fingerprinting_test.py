from younify import fingerprinter, motley
import unittest, logging


motley.setup_logger(__name__)
log = logging.getLogger(__name__)


class TestFingerprintingMethods(unittest.TestCase):
    def test_instantiation(self):
        fingerprint = fingerprinter.FingerPrinter()
        print(fingerprint)


if __name__ == '__main__':
    unittest.main()
