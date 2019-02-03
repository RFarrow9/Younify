#import time
import queue
# import sys
# import breeze_resources
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QFile, QTextStream
from threading import Thread

# from younify import frontend
from younify import youtube_converter

# Need to pick a style (camelcase?) and stick with it
# Testing to be in seperate module
# Array + gui should be split into seperate modules
# Single module to hang everything together (main?)

fetch_threads = 4
enclosure_queue = queue.Queue()
temp_processing = "C:\\Users\\robfa\\PycharmProjects\\Younify\\younify\\temp\\temp-processed.tmp"
temp_working = "C:\\Users\\robfa\\PycharmProjects\\Younify\\younify\\temp\\temp-working.tmp"
bookmarks = "working\\bookmarks.html"
bookmarks1 = "C:\\Users\\robfa\\Desktop\\bookmarks.html"

def Main():
    processed = ProcessedURLs()
    working = WorkingURLs()
    failed = FailedURLs()
    working.PushfiletoWorking(bookmarks1)
    while working.CountURLs() > 0:
        try:
            ProcessURLs(working, processed, failed)
        except:
            processed.UpdateTemp()
            working.UpdateTemp()
        finally:
            processed.UpdateTemp()
            working.UpdateTemp()


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
            print("file not found")

    def UpdateTemp(self):
        file = open(temp_processing, "w+")
        for URL in self.URLs:
            file.write(URL[-11:] + "\r")

class WorkingURLs(ProcessingArray):
    def __init__(self):
        ProcessingArray.__init__(self)
        #self.URLs = []
        try:
            file = open(temp_working, "r")
            for line in file:
                self.AddURL(line[:-1])
            file.close()
        except:
            print("file not found")

    def UpdateTemp(self):
        file = open(temp_working, "w+")
        for URL in self.URLs:
            file.write(URL[-11:] + "\r")

    def PushfiletoWorking(self, filename):
        array = FindURLsInFile(filename)
        for URL in array:
            self.AddURL(URL)

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


#
#    Functions defined below
#

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

def ProcessURL(i, q, working, processed, failed):
    while True:
        URL = q.get()
        try:
            #RunMattsCodeHere("https://www.youtube.com/watch?v=" + URL)
            youtube_converter.get_audio(["https://www.youtube.com/watch?v=" + URL], "", "")
            processed.AddURL(URL)
        except:
            #failed.AddURL(URL, 'pass through error here')
            print("error unknown")
        finally:
            working.RemoveURL(URL)
            q.task_done()

def ProcessURLs(working, processed, failed):
    for i in range(fetch_threads):
        worker = Thread(target=ProcessURL, args=(i, enclosure_queue, working, processed, failed))
        worker.setDaemon(True)
        worker.start()
    if working.CountURLs() > 0:
        for URL in working.RetrieveURLs():
            enclosure_queue.put(URL)
    enclosure_queue.join()

if __name__ == '__main__':
    Main()


