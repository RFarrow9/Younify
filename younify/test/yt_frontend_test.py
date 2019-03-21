#import time
from younify import yt_frontend
import unittest

class TestFrameworkMethods(unittest.TestCase):
    def launch_gui(self):
        yt_frontend.main()

if __name__ == '__main__':
    unittest.main()
