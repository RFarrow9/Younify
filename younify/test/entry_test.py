from younify import entry, motley
import unittest
import json
import logging

with open('c:\\config\\config.json') as f:
    config = json.load(f)

test_audio_file = config["filehandler_test"]["test_audio_file"]
motley.setup_logger(__name__)
log = logging.getLogger(__name__)

class TestEntryMethods(unittest.TestCase):
    def test_debugging(self):
        log.debug('testing debugging')



if __name__ == '__main__':
    unittest.main()

