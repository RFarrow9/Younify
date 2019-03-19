from younify import youtube_converter
import unittest

class TestConverterMethods(unittest.TestCase):

#    def test_get_audio_song(self):
#        video = youtube_converter.VideoFactory("https://www.youtube.com/watch?v=oKeCXlnL5Lg").classify()
#        print(video)
        #video.process()

    def test_get_audio_playlist(self):
        video = youtube_converter.VideoFactory("https://www.youtube.com/watch?v=eqJFVg05b8Q").classify()
        print(video)
        #video.print_desc()
 #       #video.process()

 #   def test_another(self):
 #       video = youtube_converter.VideoFactory("https://www.youtube.com/watch?v=nICgdqB7wME").classify()
 #       print(video)

if __name__ == '__main__':
    unittest.main()

