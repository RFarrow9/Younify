from younify import spotify
import unittest

class TestSpotifyMethods(unittest.TestCase):

    def test_levenshtein(self):
        self.assertTrue(spotify.levenshtein("twat", "mong") == 4)
        self.assertTrue(spotify.levenshtein("twat", "twat") == 0)

if __name__ == '__main__':
    unittest.main()