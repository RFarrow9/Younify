from younify import *

log = motley.setup_logger(__name__)

class TestConverterMethods(unittest.TestCase):

    def test_globals(self):
        print(factory.root_dir)
        print(factory.spotify_dir)
        print(factory.artwork)

    def test_get_audio_songs(self):
        tests = []
        tests.append("https://www.youtube.com/watch?v=Am9lfs7M_OQ")
        tests.append("https://www.youtube.com/watch?v=fKFbnhcNnjE")
        for test in tests:
            video = factory.VideoFactory(test).classify()
            print(video)
            video.process()

    def test_get_audio_playlist(self):
        video = factory.VideoFactory("https://www.youtube.com/watch?v=GmzWbgzo6B4").classify()
        print(video)
        video.process()


if __name__ == '__main__':
    unittest.main()

