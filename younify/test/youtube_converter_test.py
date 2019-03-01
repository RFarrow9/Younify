from younify import youtube_converter as yc
import unittest

class TestConverterMethods(unittest.TestCase):

    def test_get_audio(self):
        url = yc.Url("https://www.youtube.com/watch?v=8-fkmRaX0Wk")
        #self.assertTrue(youtube_converter.levenshtein("twat", "mong") == 4)
        #s#elf.assertTrue(youtube_converter.levenshtein("twat", "twat") == 0)
        #url.print(self)
        url.print()

    def test_convert(self):
        print("this is a placeholder")
        
if __name__ == '__main__':
    unittest.main()
