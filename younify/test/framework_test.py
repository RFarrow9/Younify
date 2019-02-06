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
temp_processing = "temp\\temp-processed.tmp"
temp_working = "temp\\temp-working.tmp"
bookmarks = "working\\Bookmarks.html"

class TestFrameworkMethods(unittest.TestCase):

    def setUp_empty(self):
        self.WorkingURLs = framework.WorkingURLs()
        self.FailedURLs = framework.FailedURLs()
        self.ProcessedURLs = framework.ProcessedURLs()
        self.WorkingURLs.TruncateURLs()
        self.ProcessedURLs.TruncateURLs()
        self.FailedURLs.TruncateURLs()

    def setUp_populated(self):
        self.WorkingURLs = framework.WorkingURLs()
        self.FailedURLs = framework.FailedURLs()
        self.ProcessedURLs = framework.ProcessedURLs()

    def tearDown(self):
        self.WorkingURLs.TruncateURLs()
        self.FailedURLs.TruncateURLs()
        self.ProcessedURLs.TruncateURLs()

    def test_instantiated(self):
        self.setUp_populated()
        self.assertTrue(self.WorkingURLs.CountURLs() > 1200)
        self.assertTrue(self.ProcessedURLs.CountURLs() >= 2)
        self.assertEqual(self.FailedURLs.CountURLs(), 0)
        self.tearDown()

    def test_truncate(self):
        self.setUp_populated()
        self.WorkingURLs.TruncateURLs()
        self.ProcessedURLs.TruncateURLs()
        self.FailedURLs.TruncateURLs()
        self.assertEqual(self.WorkingURLs.CountURLs(), 0)
        self.assertEqual(self.ProcessedURLs.CountURLs(), 0)
        self.assertEqual(self.FailedURLs.CountURLs(), 0)
        self.tearDown()

    def test_fileparse(self):
        self.setUp_empty()
        list = framework.FindURLsInFile(bookmarks)
        self.WorkingURLs.PushfiletoWorking(bookmarks)
        self.assertTrue(len(list) > 1200, len(list))
        self.assertTrue(self.WorkingURLs.CountURLs() > 1200, self.WorkingURLs.CountURLs())
        self.assertEqual(self.WorkingURLs.CountURLs(), len(list))
        self.tearDown()

    def test_processing(self):
        self.setUp_empty()
        WorkingCount = self.WorkingURLs.CountURLs()
        self.framework.ProcessURL("YSkIJTIE45c")
        self.WorkingURLs.ProcessURL__old("YSkIJTIE45c") #dOESNT WORK YET
        self.WorkingURLs.ProcessURL__old("B2KAipyP8mc")
        self.assertTrue(self.WorkingURLs.CountURLs() + 2, WorkingCount)
        #self.assertTrue()

    def test_fails(self):
        self.setUp_empty()
        self.assertEqual(self.FailedURLs.CountURLs(), 0)
        self.FailedURLs.AddURL("B2KAipyP8mc", 'test')
        self.FailedURLs.AddURL("B2KgipyP8mc", '2nd error')
        self.FailedURLs.AddURL("B2KAipyP8mc", '3rd error')
        self.assertEqual(self.FailedURLs.CountURLs(), 2)
        self.tearDown()

    def test_updatetemp(self):
        self.setUp_empty()
        self.WorkingURLs.PushfiletoWorking(bookmarks)
        WorkingCount = self.WorkingURLs.CountURLs()
        self.assertTrue(WorkingCount > 1200)
        self.WorkingURLs.UpdateTemp()
        self.assertEqual(WorkingCount, linecount(temp_working))
        self.WorkingURLs.ProcessURL__old("YSkIJTIE45c") #dOESNT WORK YET
        self.WorkingURLs.ProcessURL__old("B2KAipyP8mc")
        self.assertEqual(WorkingCount - 2, linecount(bookmarks))
        self.assertEqual(self.ProcessedURLs.CountURLs(), 2)
        self.ProcessedURLs.UpdateTemp()
        self.asssertEqual(linecount(temp_processing), 2)

    def test_retrievetemp(self):
        self.setUp_empty()
        self.WorkingURLs.PushfiletoWorking(bookmarks)
        self.WorkingURLs.UpdateTemp()
        temp_working_linecount = linecount(temp_working)
        self.assertTrue(temp_working_linecount > 1200)
        self.WorkingURLs.__init__()
        self.assertEqual(temp_working_linecount, self.WorkingURls.CountURLs())

    def test_retrievemultiples(self):
        self.setUp_empty()
        self.WorkingURLs.PushfiletoWorking(bookmarks)
        self.WorkingURLs.UpdateTemp()
        temp_working_linecount = linecount(temp_working)


if __name__ == '__main__':
    unittest.main()

