from younify import *

log = motley.setup_logger(__name__)


class TestEntryMethods(unittest.TestCase):
    def test_debugging(self):
        log.debug('testing debugging')

    def test_everything(self):
        working.push_file_to_working(bookmarks)
        working.push_urls_to_queue()
        working.process_urls(processed)


if __name__ == '__main__':
    unittest.main()

