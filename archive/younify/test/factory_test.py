from younify import *

log = motley.setup_logger(__name__)


class TestConverterMethods(unittest.TestCase):
    def test_get_audio_songs(self):
        tests = []
        tests.append("https://www.youtube.com/watch?v=Am9lfs7M_OQ")
        tests.append("https://www.youtube.com/watch?v=fKFbnhcNnjE")
        for test in tests:
            video = factory.VideoFactory(test).classify()
            video.log()
            video.process()

    def test_get_audio_playlist(self):
        video = factory.VideoFactory("https://www.youtube.com/watch?v=GmzWbgzo6B4").classify()
        video.log()
        video.process()

    def test_classification(self):
        test = "https://www.youtube.com/watch?v=fKFbnhcNnjE"
        test2 = ""
        instance = factory.VideoFactory(test).classify()
        instance2 = factory.VideoFactory(test2).classify()
        self.assertTrue(instance.type == "YoutubeSong")
        self.assertTrue(instance2.type == "YoutubePlaylist")


if __name__ == '__main__':
    unittest.main()

