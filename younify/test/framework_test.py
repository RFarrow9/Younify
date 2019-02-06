#import time
from younify import framework
import unittest

# Need to pick a style (camelcase?) and stick with it
# Testing to be in seperate module
# Array + gui should be split into seperate modules
# Single module to hang everything together (main?)
#testing successful commit

fetch_threads = 4
#enclosure_queue = queue.Queue()
temp_processing = "..\\temp\\temp-processed.tmp"
temp_working = "..\\temp\\temp-working.tmp"
bookmarks = "C:\\Users\\robfa\\PycharmProjects\\Younify\\younify\\test\\working\\bookmarks.html"

class TestFrameworkMethods(unittest.TestCase):

    def setUp_empty(self):
        self.WorkingURLs = framework.WorkingURLs()
        self.FailedURLs = framework.FailedURLs()
        self.ProcessedURLs = framework.ProcessedURLs()
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()

    def setUp_populated(self):
        self.WorkingURLs = framework.WorkingURLs()
        self.FailedURLs = framework.FailedURLs()
        self.ProcessedURLs = framework.ProcessedURLs()

    def tearDown(self):
        self.WorkingURLs.truncate_urls()
        self.FailedURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()

    def test_instantiated(self):
        self.setUp_populated()
        self.assertTrue(self.WorkingURLs.count_urls() > 1200)
        self.assertTrue(self.ProcessedURLs.count_urls() >= 2)
        self.assertEqual(self.FailedURLs.count_urls(), 0)
        self.tearDown()

    def test_truncate(self):
        self.setUp_populated()
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()
        self.assertEqual(self.WorkingURLs.count_urls(), 0)
        self.assertEqual(self.ProcessedURLs.count_urls(), 0)
        self.assertEqual(self.FailedURLs.count_urls(), 0)
        self.tearDown()

    def test_fileparse(self):
        self.setUp_empty()
        urllist = framework.find_urls_in_file(bookmarks)
        self.WorkingURLs.push_file_to_working(bookmarks)
        self.assertTrue(len(urllist) > 1200, len(urllist))
        self.assertTrue(self.WorkingURLs.count_urls() > 1200, self.WorkingURLs.count_urls())
        self.assertEqual(self.WorkingURLs.count_urls(), len(urllist))
        self.tearDown()

    def test_processing(self):
        self.setUp_empty()
        working_count = self.WorkingURLs.count_urls()
        self.assertTrue(working_count == 0)
        self.WorkingURLs.push_url_to_queue("YSkIJTIE45c")
        self.WorkingURLs.push_url_to_queue("B2KAipyP8mc")
        self.assertEqual(2, self.WorkingURLs.count_urls())
        self.WorkingURLs.process_urls(self.ProcessedURLs, self.FailedURLs)
        self.assertEqual(0, working_count)

    def test_fails(self):
        self.setUp_empty()
        self.assertEqual(self.FailedURLs.count_urls(), 0)
        self.FailedURLs.add_url("B2KAipyP8mc", 'test')
        self.FailedURLs.add_url("B2KgipyP8mc", '2nd error')
        self.FailedURLs.add_url("B2KAipyP8mc", '3rd error')
        self.assertEqual(self.FailedURLs.count_urls(), 2)
        self.tearDown()

    def test_updatetemp(self):
        self.setUp_empty()
        self.WorkingURLs.push_file_to_working(bookmarks)
        working_count = self.WorkingURLs.count_urls()
        self.assertTrue(working_count > 1200)
        self.WorkingURLs.update_temp()
        self.assertEqual(working_count, framework.linecount(temp_working))
        self.WorkingURLs.add_url("YSkIJTIE45c")
        self.WorkingURLs.add_url("B2KAipyP8mc")
        self.WorkingURLs.process_url("YSkIJTIE45c", self.ProcessedURLs)
        self.WorkingURLs.process_url("B2KAipyP8mc", self.ProcessedURLs)
        self.assertEqual(working_count - 2, framework.linecount(bookmarks))
        self.assertEqual(self.ProcessedURLs.count_urls(), 2)
        self.ProcessedURLs.update_temp()
        self.assertEqual(framework.linecount(temp_processing), 2)

    def test_retrievetemp(self):
        self.setUp_empty()
        self.WorkingURLs.push_file_to_working(bookmarks)
        self.WorkingURLs.update_temp()
        temp_working_linecount = framework.linecount(temp_working)
        self.assertTrue(temp_working_linecount > 1200)
        self.WorkingURLs.__init__()
        self.assertEqual(temp_working_linecount, self.WorkingURLs.count_urls())

    def test_retrievemultiples(self):
        self.setUp_empty()
        self.WorkingURLs.push_file_to_working(bookmarks)
        self.WorkingURLs.update_temp()
        temp_working_linecount = framework.linecount(temp_working)


if __name__ == '__main__':
    unittest.main()

