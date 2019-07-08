from younify import *

log = motley.setup_logger(__name__)

class TestEntryMethods(unittest.TestCase):
    def test_debugging(self):
        log.debug('testing debugging')



if __name__ == '__main__':
    unittest.main()

