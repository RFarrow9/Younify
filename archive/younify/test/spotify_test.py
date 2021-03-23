from younify import *

log = motley.setup_logger(__name__)


class TestSpotifyMethods(unittest.TestCase):
    def test_levenshtein(self):
        self.assertTrue(spotify.levenshtein("cat", "dog") == 3)
        self.assertTrue(spotify.levenshtein("dog", "dog") == 0)

    def test_cleantitle(self):
        raise NotImplemented()

    def test_consecutive_groups(self):
        generator = spotify.consecutive_groups()
        self.assertTrue(sum(1 for i in generator)==15, sum(1 for i in generator))
        generator2 = spotify.consecutive_groups("test string2")
        self.assertTrue(sum(1 for i in generator2)==3, sum(1 for i in generator2))
        generator3 = spotify.consecutive_groups("1 2 3 4 5 6 7 8 9 10")
        self.assertTrue(sum(1 for i in generator3)==55, sum(1 for i in generator3))

    def test_extraction(self):
        tests = []
        #tests.append("Billy Corgan & Mike Garson // Orah / Random Thought (from \"Stigmata\") [1999]")
        tests.append("The killers - Human")
        for test in tests:
            extractor = spotify.SpotifyMatching(test)
            extractor.process()

    def test_SpotifyProcessing_instantiation(self):
        raise NotImplemented()

    def test_SpotifyProcessing_artist_song_first_pass(self):
        raise NotImplemented()

    def test_SpotifyProcessing_artist_second_pass(self):
        raise NotImplemented()

    def test_SpotifyProcessing_artist_song_second_pass(self):
        raise NotImplemented()

    def test_SpotifyProcessing_all_songs(self):
        raise NotImplemented()

    def test_SpotifyProcessing_all_albums(self):
        raise NotImplemented()

    def test_clean(self):
        raise NotImplemented()

    def test_most_common(self):
        raise NotImplemented()


if __name__ == '__main__':
    unittest.main()
