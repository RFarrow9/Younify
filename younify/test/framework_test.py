#import time
from younify import framework
import unittest

# Need to pick a style (camelcase?) and stick with it
# Testing to be in seperate module
# Array + gui should be split into seperate modules
# Single module to hang everything together (main?)

fetch_threads = 4
#enclosure_queue = queue.Queue()
temp_processing = "temp\\temp-processed.tmp"
temp_working = "temp\\temp-working.tmp"
bookmarks = "test\\working\\Bookmarks.html"

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
        self.WorkingURLs.ProcessURL__old("YSkIJTIE45c") #dOESNT WORK YET
        self.WorkingURLs.ProcessURL__old("B2KAipyP8mc")
        self.AssertTrue(self.WorkingURLs.CountURLs() + 2, WorkingCount)
        self.assertTrue()

    def test_fails(self):
        self.setUp_empty()
        self.AssertEqual(self.FailedURLs.CountURLs(), 0)
        FailedURLs.AddURL("B2KAipyP8mc", 'test')
        FailedURLs.AddURL("B2KgipyP8mc", '2nd error')
        FailedURLs.AddURL("B2KAipyP8mc", '3rd error')
        self.AssertEqual(self.FailedURLs.CountURLs(), 0)
        self.tearDown()

    def test_updatetemp(self):
        self.setUp_empty()
        self.WorkingURLs.PushfiletoWorking(bookmarks)
        WorkingCount = self.WorkingURLs.CountURLS()
        self.AssertTrue(WorkingCount > 1200)
        self.WorkingURLs.UpdateTemp()
        self.AssertEquals(WorkingCount, linecount(temp_working))
        self.WorkingURLs.ProcessURL__old("YSkIJTIE45c") #dOESNT WORK YET
        self.WorkingURLs.ProcessURL__old("B2KAipyP8mc")
        self.AssertEquals(WorkingCount - 2, linecount(bookmarks))
        self.AssertEquals(self.ProcessedURLs.CountURLs(), 2)
        self.ProcessedURLs.UpdateTemp()
        self.AsssertEquals(linecount(temp_processing), 2)

    def test_retrievetemp(self):
        self.setUp_empty()
        self.WorkingURLs.PushfiletoWorking(bookmarks)
        self.WorkingURLs.UpdateTemp()
        temp_working_linecount = linecount(temp_working)
        self.assertTrue(temp_working_linecount > 1200)
        self.WorkingURLs.__init__()
        self.assertEquals(temp_working_linecount, self.WorkingURls.CountURLs())

    def test_retrievemultiples(self):
        self.setUp_empty()
        self.WorkingURLs.PushfiletoWorking(bookmarks)
        self.WorkingURLs.UpdateTemp()
        temp_working_linecount = linecount(temp_working)


if __name__ == '__main__':
    unittest.main()


#    WorkingURLs = WorkingURLs()
#    ProcessedURLs = ProcessedURLs()
#    FailedURLs = FailedURLs()

#    print("")
#    print("======= UNIT TESTING =======")
#    WorkingURLs.TruncateURLs()
#    FailedURLs.TruncateURLs()
#    ProcessedURLs.TruncateURLs()
#    if ProcessedURLs.CountURLs() == WorkingURLs.CountURLs() == FailedURLs.CountURLs() == 0:
#        print("TESTING LIST TRUNCATION:             PASS")
#    else:
#        print("TESTING LIST TRUNCATION:             FAIL")
#    list = FindURLsInFile(bookmarks)
#    PushfiletoWorking(bookmarks)
#    if len(list) == WorkingURLs.CountURLs() == 1495:
#        print("TESTING FILE RETRIEVAL:              PASS")
#    else:
#        print("TESTING FILE RETRIEVAL:              FAIL")
#        print("     URLS IN FILE: " + str(len(list)))
#        print("     URLS IN LIST: " + str(WorkingURLs.CountURLs()))
#    ProcessURL__old("YSkIJTIE45c")
#    ProcessURL__old("B2KAipyP8mc")
#    FailedURLs.AddURL("B2KAipyP8mc", 'test')
#    FailedURLs.AddURL("B2KgipyP8mc", '2nd error')
#    FailedURLs.AddURL("B2KAipyP8mc", '3rd error')
#    if ProcessedURLs.CountURLs() == 2 and FailedURLs.CountURLs() == 2 and WorkingURLs.CountURLs() == 1493:
#        print("TESTING URL PROCESSING:              PASS")
#    else:
#        print("TESTING URL PROCESSING:              FAIL")
#        print("     WORKING URLS:    " + str(WorkingURLs.CountURLs()))
#        print("     FAILED URLS:     " + str(FailedURLs.CountURLs()))
#        print("     PROCESSED URLS:  " + str(ProcessedURLs.CountURLs()))
#    WorkingURLs.UpdateTemp()
#    ProcessedURLs.UpdateTemp()
#    if linecount(temp_processing) == 2 and linecount(temp_working) == 1493:
#        print("TESTING TEMP FILE GENERATION:        PASS")
##    else:
#        print("TESTING TEMP FILE GENERATION:        FAIL")
#        print("     WORKING TEMP FILE:   " + str(linecount(temp_working)))
#        print("     PROCESSED TEMP FILE: " + str(linecount(temp_processing)))
#    WorkingURLs.UpdateTemp()
#    ProcessedURLs.UpdateTemp()
    if linecount(temp_processing) == 2 and linecount(temp_working) == 1493:
        print("TESTING 2ND FILE GENERATION:         PASS")
    else:
        print("TESTING 2ND FILE GENERATION:         FAIL")
        print("     WORKING TEMP FILE:   " + str(linecount(temp_working)))
        print("     PROCESSED TEMP FILE: " + str(linecount(temp_processing)))
    WorkingURLs.RemoveURL("WQzZk69P69E")
    if WorkingURLs.CountURLs() == 1492:
        print("TESTING URL REMOVAL:                 PASS")
    else:
        print("TESTING URL REMOVAL:                 FAIL")
        print("     WORKING URLS:    " + str(WorkingURLs.CountURLs()))
    WorkingURLs.TruncateURLs()
    FailedURLs.TruncateURLs()
    ProcessedURLs.TruncateURLs()
    WorkingURLs.__init__()
    ProcessedURLs.__init__()
    if ProcessedURLs.CountURLs() == 2 and WorkingURLs.CountURLs() == 1493 and FailedURLs.CountURLs() == 0:
        print("TESTING TEMP FILE RETRIEVAL:         PASS")
    else:
        print("TESTING TEMP FILE RETRIEVAL:         FAIL")
        print("     WORKING URLS:    " + str(WorkingURLs.CountURLs()))
        print("     PROCESSED URLS:  " + str(ProcessedURLs.CountURLs()))
    ProcessURLs()
    if ProcessedURLs.CountURLs() == 1495 and WorkingURLs.CountURLs() == 0 and FailedURLs.CountURLs() == 0:
        print("TESTING MULTITHREADING QUEUE:        PASS")
    else:
        print("TESTING MULTITHREADING QUEUE:        FAIL")
        print("     WORKING URLS:    " + str(WorkingURLs.CountURLs()))
        print("     PROCESSED URLS:  " + str(ProcessedURLs.CountURLs()))
        print("     FAILED URLS:     " + str(FailedURLs.CountURLs()))
    print("======= /UNIT TESTING =======")
    print("")
    print("======== GUI TESTING ========")
    RunMain()


    #Cleaning up
    WorkingURLs.TruncateURLs()
    FailedURLs.TruncateURLs()
    ProcessedURLs.TruncateURLs()
    WorkingURLs.UpdateTemp()
    ProcessedURLs.UpdateTemp()
