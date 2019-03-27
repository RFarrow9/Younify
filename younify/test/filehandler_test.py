from younify import filehandler
import unittest
import json

with open('c:\\config\\config.json') as f:
    config = json.load(f)

test_audio_file = config["filehandler_test"]["test_audio_file"]

class TestFileHandlerMethods(unittest.TestCase):

    def test_instantiation(self):
        file = filehandler.FileHandler(test_audio_file)
        print(file)

    def test_first_pass(self):
        file = filehandler.FileHandler(test_audio_file)
        file.first_pass()
        #Need to make sure this equality is case insensitive
        self.assertTrue(file.artist, "Rick Astley")
        self.assertTrue(file.title, "Never gonna give you up")

    def test_second_pass(self):
        file = filehandler.FileHandler(test_audio_file)
        file.second_pass()
        #Put assertions below

    def test_third_pass(self):
        file = filehandler.FileHandler(test_audio_file)
        file.third_pass()
        #Put assertions below
        #Make sure this file contains data to be fingerprinted

if __name__ == '__main__':
    unittest.main()
