from younify import alchemy
import unittest
import json

with open('c:\\config\\config.json') as f:
    config = json.load(f)

test_audio_file = config["filehandler_test"]["test_audio_file"]


class TestFileHandlerMethods(unittest.TestCase):

    def reset_to_default(self):
        alchemy.

    def test_object_instantiation(self):
        Song = alchemy.FileHandler(test_audio_file)
        print(file)

if __name__ == '__main__':
    unittest.main()
