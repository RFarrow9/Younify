from younify import alchemy, motley
import unittest
import logging
import json

with open('c:\\config\\config.json') as f:
    config = json.load(f)

test_audio_file = config["filehandler_test"]["test_audio_file"]
motley.setup_logger(__name__)
log = logging.getLogger(__name__)

class TestFileHandlerMethods(unittest.TestCase):
    def reset_to_default(self):
        log.debug('priming database')
        alchemy.prime()

    def test_object_instantiation(self):
        log.debug('instantiating alchemy song')
        test_song = alchemy.Song()
        print(test_song)


if __name__ == '__main__':
    unittest.main()
