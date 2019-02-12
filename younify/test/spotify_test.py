from younify import spotify
import unittest

class TestSpotifyMethods(unittest.TestCase):

    def test_levenshtein(self):
        self.assertTrue(spotify.levenshtein("twat", "mong") == 4)
        self.assertTrue(spotify.levenshtein("twat", "twat") == 0)

    def test_cleantitle(self):
        print("this is a placeholder")

    def test_consecutive_groups(self):
        generator = spotify.consecutive_groups()
        self.assertTrue(sum(1 for i in generator)==15, sum(1 for i in generator))
        generator2 = spotify.consecutive_groups("test string2")
        self.assertTrue(sum(1 for i in generator2)==3, sum(1 for i in generator2))
        generator3 = spotify.consecutive_groups("1 2 3 4 5 6 7 8 9 10")
        self.assertTrue(sum(1 for i in generator3)==55, sum(1 for i in generator3))

if __name__ == '__main__':
    unittest.main()
