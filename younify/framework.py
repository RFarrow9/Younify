#import time
import queue
import sys
#import breeze_resources
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream
from threading import Thread
from frontend import Ui_MainWindow

# Need to pick a style (camelcase?) and stick with it
# Testing to be in seperate module
# Array + gui should be split into seperate modules
# Single module to hang everything together (main?)

fetch_threads = 4
enclosure_queue = queue.Queue()
temp_processing = "temp\\temp-processed.tmp"
temp_working = "temp\\temp-working.tmp"
bookmarks = "working\\Bookmarks.html"

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def RunMain():
    app = QtWidgets.QApplication([])
    file = QFile("resources\\dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    application = mywindow()
    application.show()
    sys.exit(app.exec())

class ProcessingArray:
    def __new__(cls, *args, **kwargs):
        if cls is ProcessingArray:
                raise TypeError("base class may not be instantiated")
        return object.__new__(cls, *args, **kwargs)

    def __init__(self):
        self.URLs = []

    def AddURL(self, URL):
        if URL not in self.URLs:
            self.URLs.append(URL)

    def CountURLs(self):
        return len(self.URLs)

    def RemoveURL(self, URL):
        if URL in self.URLs:
            self.URLs.remove(URL)

    def TruncateURLs(self):
        self.URLs = []

    def PrintSample(self):
        print(self.URLs[0: 5])

    def RetrieveURLs(self):
        return self.URLs

class ProcessedURLs(ProcessingArray):
    def __init__(self):
        ProcessingArray.__init__(self)
        try:
            file = open(temp_processing, "r")
            for line in file:
                self.AddURL(line[:-1])
            file.close()
        except:
            pass

    def UpdateTemp(self):
        file = open(temp_processing, "w+")
        for URL in self.URLs:
            file.write(URL[-11:] + "\r")

class WorkingURLs(ProcessingArray):
    def __init__(self):
        ProcessingArray.__init__(self)
        try:
            file = open(temp_working, "r")
            for line in file:
                self.AddURL(line[:-1])
            file.close()
        except:
            pass

    def UpdateTemp(self):
        file = open(temp_working, "w+")
        for URL in self.URLs:
            file.write(URL[-11:] + "\r")

    def PushfiletoWorking(self, filename):
        array = FindURLsInFile(filename)
        for URL in array:
            self.AddURL(URL)

    def ProcessURLs_OLD(self):
        while self.CountURLs() > 0:
            for URL in self.RetrieveURLs():
                ProcessURL(URL)

    def ProcessURL__old(self, URL): #THIS FUNCTION AINT USED NO MORE
        try:
            #RunMattsCodeHere("https://www.youtube.com/watch?v=" + URL)
            ProcessedURLs.AddURL(URL)
        except:
            FailedURLs.AddURL(URL, "ERROR PLACEHOLDER")
        finally:
            self.RemoveURL(URL)

class FailedURLs():
    def __init__(self):
        self.URLs = []

    def AddURL(self, URL, error):
        if len(self.URLs) == 0:
            self.URLs.append([URL, error])
        else:
            for pair in self.URLs:
                if URL in pair:
                    break
                else:
                    self.URLs.append([URL, error])

    def CountURLs(self):
        return len(self.URLs)

    def RemoveURL(self, URL):
        for pair in self.URLs:
            if URL in pair[0]:
                self.URLs.remove(pair)

    def TruncateURLs(self):
        self.URLs = []

    def PrintSample(self):
        print(self.URLs[0: 5])

def linecount(filename):
  count = 0
  for line in open (filename):
    count += 1
  return count

def FindURLsInFile(filename):
    count, URLs = 0, []
    try:
        for line in open(filename, encoding = 'utf8'):
            list = FindURL(line)
            count += list[0]
            if list[0] > 0:
                for URL in list[1]:
                    if URL not in URLs:
                        URLs.append(URL)
    except IOError:
        print("file not found")
    except:
        print("There was a generic error")
    return URLs

def FindURL(string):
#Could this function be generalised? What about other providers (soundcloud, vimeo etc)
    count, URL, array = 0, '', []
    index = string.find('https://www.youtube.com/watch?v=')
    URL = string[index+32:index+43]
    if index >= 0:
        count += 1
        array.append(URL)
        FindURL(string[index+43:])
    return count, array

def ProcessURL__old(URL): #THIS FUNCTION AINT USED NO MORE
    try:
        #RunMattsCodeHere("https://www.youtube.com/watch?v=" + URL)
        ProcessedURLs.AddURL(URL)
    except:
        FailedURLs.AddURL(URL, 'pass through error here')
    finally:
        WorkingURLs.RemoveURL(URL)

def ProcessURLs_OLD(): #NEITHER THIS BAD BOY
    while WorkingURLs.CountURLs() > 0:
        for URL in WorkingURLs.RetrieveURLs():
            ProcessURL(URL)

#Defines worker
def ProcessURL(i, q):
    while True:
        URL = q.get()
        try:
            #RunMattsCodeHere("https://www.youtube.com/watch?v=" + URL)
            ProcessedURLs.AddURL(URL)
        except:
            FailedURLs.AddURL(URL, 'pass through error here')
        finally:
            WorkingURLs.RemoveURL(URL)
            q.task_done()

#
def ProcessURLs():
    for i in range(fetch_threads):
        worker = Thread(target=ProcessURL, args=(i, enclosure_queue,))
        worker.setDaemon(True)
        worker.start()
    while WorkingURLs.CountURLs() > 0:
        for URL in WorkingURLs.RetrieveURLs():
            enclosure_queue.put(URL)
    enclosure_queue.join()

if __name__ == '__main__':

    WorkingURLs = WorkingURLs()
    ProcessedURLs = ProcessedURLs()
    FailedURLs = FailedURLs()
    print("")
    print("======= UNIT TESTING =======")
    WorkingURLs.TruncateURLs()
    FailedURLs.TruncateURLs()
    ProcessedURLs.TruncateURLs()
    if ProcessedURLs.CountURLs() == WorkingURLs.CountURLs() == FailedURLs.CountURLs() == 0:
        print("TESTING LIST TRUNCATION:             PASS")
    else:
        print("TESTING LIST TRUNCATION:             FAIL")
    list = FindURLsInFile(bookmarks)
    PushfiletoWorking(bookmarks)
    if len(list) == WorkingURLs.CountURLs() == 1495:
        print("TESTING FILE RETRIEVAL:              PASS")
    else:
        print("TESTING FILE RETRIEVAL:              FAIL")
        print("     URLS IN FILE: " + str(len(list)))
        print("     URLS IN LIST: " + str(WorkingURLs.CountURLs()))
    ProcessURL__old("YSkIJTIE45c")
    ProcessURL__old("B2KAipyP8mc")
    FailedURLs.AddURL("B2KAipyP8mc", 'test')
    FailedURLs.AddURL("B2KgipyP8mc", '2nd error')
    FailedURLs.AddURL("B2KAipyP8mc", '3rd error')
    if ProcessedURLs.CountURLs() == 2 and FailedURLs.CountURLs() == 2 and WorkingURLs.CountURLs() == 1493:
        print("TESTING URL PROCESSING:              PASS")
    else:
        print("TESTING URL PROCESSING:              FAIL")
        print("     WORKING URLS:    " + str(WorkingURLs.CountURLs()))
        print("     FAILED URLS:     " + str(FailedURLs.CountURLs()))
        print("     PROCESSED URLS:  " + str(ProcessedURLs.CountURLs()))
    WorkingURLs.UpdateTemp()
    ProcessedURLs.UpdateTemp()
    if linecount(temp_processing) == 2 and linecount(temp_working) == 1493:
        print("TESTING TEMP FILE GENERATION:        PASS")
    else:
        print("TESTING TEMP FILE GENERATION:        FAIL")
        print("     WORKING TEMP FILE:   " + str(linecount(temp_working)))
        print("     PROCESSED TEMP FILE: " + str(linecount(temp_processing)))
    WorkingURLs.UpdateTemp()
    ProcessedURLs.UpdateTemp()
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
