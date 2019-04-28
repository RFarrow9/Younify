from younify import youtube_converter
import unittest

class TestConverterMethods(unittest.TestCase):

    def test_globals(self):
        print(youtube_converter.root_dir)
        print(youtube_converter.spotify_dir)
        print(youtube_converter.artwork)

    def test_get_audio_songs(self):
        tests = []
        tests.append("https://www.youtube.com/watch?v=Am9lfs7M_OQ")
        tests.append("https://www.youtube.com/watch?v=fKFbnhcNnjE")
        for test in tests:
            video = youtube_converter.VideoFactory(test).classify()
            print(video)
            video.process()

    def test_get_audio_playlist(self):
        video = youtube_converter.VideoFactory("https://www.youtube.com/watch?v=GmzWbgzo6B4").classify()
        print(video)
        video.process()


if __name__ == '__main__':
    unittest.main()

