from younify import *

log = motley.setup_logger(__name__)

class TestFrameworkMethods(unittest.TestCase):
    def setup_empty(self):
        log.debug('setting up empty frames')
        self.WorkingURLs = frames.working
        self.FailedURLs = frames.failed
        self.ProcessedURLs = frames.processed
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()

    def setup_populated(self):
        self.WorkingURLs = frames.working
        self.FailedURLs = frames.failed
        self.ProcessedURLs = frames.processed

    def teardown(self):
        self.WorkingURLs.truncate_urls()
        self.FailedURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()

    def test_instantiated(self):
        self.setup_populated()
        linecount_working = frames.linecount(temp_working)
        linecount_processed = frames.linecount(temp_processing)
        linecount_failed = frames.linecount(temp_failed)
        self.assertTrue(self.WorkingURLs.count_urls() == linecount_working, self.WorkingURLs.count_urls())
        self.assertTrue(self.ProcessedURLs.count_urls() == linecount_processed, self.ProcessedURLs.count_urls())
        self.assertTrue(self.FailedURLs.count_urls() == linecount_failed, self.FailedURLs.count_urls())
        self.teardown()

    def test_truncate(self):
        self.setup_populated()
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()
        self.assertEqual(self.WorkingURLs.count_urls(), 0, self.WorkingURLs.count_urls())
        self.assertEqual(self.ProcessedURLs.count_urls(), 0, self.ProcessedURLs.count_urls())
        self.assertEqual(self.FailedURLs.count_urls(), 0, self.FailedURLs.count_urls())
        self.teardown()

    def test_fileparse(self):
        self.setup_empty()
        urllist = frames.find_urls_in_file(bookmarks)
        self.WorkingURLs.push_file_to_working(bookmarks)
        self.assertTrue(len(urllist) > 1200, len(urllist))
        self.assertTrue(self.WorkingURLs.count_urls() > 1200, self.WorkingURLs.count_urls())
        self.assertEqual(self.WorkingURLs.count_urls(), len(urllist))
        self.teardown()

#    def test_processing(self):
#        self.setup_empty()
#        working_count = self.WorkingURLs.count_urls()
#        self.assertTrue(working_count == 0)
#        self.WorkingURLs.push_url_to_queue("YSkIJTIE45c")
#        self.WorkingURLs.push_url_to_queue("B2KAipyP8mc")
#        self.assertEqual(2, self.WorkingURLs.count_urls())
#        self.WorkingURLs.process_urls(self.ProcessedURLs, self.FailedURLs)
#        self.assertEqual(0, working_count)
#        self.teardown()

    def test_fails(self):
        self.setup_empty()
        self.assertEqual(self.FailedURLs.count_urls(), 0)
        self.FailedURLs.add_url("B2KAipyP8mc", 'test')
        self.FailedURLs.add_url("B2KgipyP8mc", '2nd error')
        self.FailedURLs.add_url("B2KAipyP8mc", '3rd error')
        self.assertEqual(self.FailedURLs.count_urls(), 2)
        self.teardown()

#    def test_updatetemp(self):
#        self.setup_empty()
#        self.WorkingURLs.push_file_to_working(bookmarks)
#        working_count = self.WorkingURLs.count_urls()
#        self.assertTrue(working_count > 1200)
#        self.WorkingURLs.update_temp()
#        self.assertEqual(working_count, framework.linecount(temp_working))
#        self.WorkingURLs.add_url("YSkIJTIE45c")
#        self.WorkingURLs.add_url("B2KAipyP8mc")
#        self.WorkingURLs.process_url("YSkIJTIE45c", self.ProcessedURLs)
#        self.WorkingURLs.process_url("B2KAipyP8mc", self.ProcessedURLs)
#        self.assertEqual(working_count - 2, framework.linecount(bookmarks))
#        self.assertEqual(self.ProcessedURLs.count_urls(), 2)
#        self.ProcessedURLs.update_temp()
#        self.assertEqual(framework.linecount(temp_processing), 2)

    def test_retrievetemp(self):
        self.setup_empty()
        self.WorkingURLs.push_file_to_working(bookmarks)
        self.WorkingURLs.update_temp()
        temp_working_linecount = frames.linecount(temp_working)
        self.assertTrue(temp_working_linecount > 1200)
        self.WorkingURLs.__init__()
        self.assertEqual(temp_working_linecount, self.WorkingURLs.count_urls())

#    def test_retrievemultiples(self):
#        self.setup_empty()
#        self.WorkingURLs.push_file_to_working(bookmarks)
#        self.WorkingURLs.update_temp()
#        temp_working_linecount = framework.linecount(temp_working)

if __name__ == '__main__':
    unittest.main()
