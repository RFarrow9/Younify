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

def main():
    processed = ProcessedURLs()
    working = WorkingURLs()
    failed = FailedURLs()
    working.push_file_to_working(bookmarks1)
    while working.count_urls() > 0:
        try:
            process_urls(working, processed, failed)
        except:
            processed.update_temp()
            working.update_temp()
        finally:
            processed.update_temp()
            working.update_temp()


class ProcessingArray:
    def __new__(cls, *args, **kwargs):
        if cls is ProcessingArray:
                raise TypeError("base class may not be instantiated")
        return object.__new__(cls, *args, **kwargs)

    def __init__(self):
        self.urls = []

    def add_url(self, url):
        if url not in self.urls:
            self.urls.append(url)

    def count_urls(self):
        return len(self.urls)

    def remove_url(self, url):
        if url in self.urls:
            self.urls.remove(url)

    def truncate_urls(self):
        self.urls = []

    def print_sample(self):
        print(self.urls[0: 5])

    def retrieve_urls(self):
        return self.urls

class ProcessedURLs(ProcessingArray):
    def __init__(self):
        ProcessingArray.__init__(self)
        try:
            file = open(temp_processing, "r")
            for line in file:
                self.add_url(line[:-1])
            file.close()
        except:
            print("file not found")

    def update_temp(self):
        file = open(temp_processing, "w+")
        for URL in self.urls:
            file.write(URL[-11:] + "\r")

class WorkingURLs(ProcessingArray):
    def __init__(self):
        ProcessingArray.__init__(self)
        try:
            file = open(temp_working, "r")
            for line in file:
                self.add_url(line[:-1])
            file.close()
        except:
            print("file not found")

    def update_temp(self):
        file = open(temp_working, "w+")
        for URL in self.urls:
            file.write(URL[-11:] + "\r")

    def push_file_to_working(self, filename):
        array = find_urls_in_file(filename)
        for url in array:
            self.add_url(url)

    def push_url_to_queue(self, url):
        if url not in self.retrieve_urls():
            enclosure_queue.put(url)

    def push_urls_to_queue(self):
        if self.count_urls() > 0:
            for url in self.retrieve_urls():
                enclosure_queue.put(url)


class FailedURLs:
    def __init__(self):
        self.urls = []

    def add_url(self, url, error):
        if len(self.urls) == 0:
            self.urls.append([url, error])
        else:
            for pair in self.urls:
                if url in pair:
                    break
                else:
                    self.urls.append([url, error])

    def count_urls(self):
        return len(self.urls)

    def remove_url(self, url):
        for pair in self.urls:
            if url in pair[0]:
                self.urls.remove(pair)

    def truncate_urls(self):
        self.urls = []

    def print_sample(self):
        print(self.urls[0: 5])

#
#    Functions defined below
#

def linecount(filename):
  count = 0
  for line in open (filename):
    count += 1
  return count

def find_urls_in_file(filename):
    count, urls = 0, []
    try:
        for line in open(filename, encoding = 'utf8'):
            list = find_url(line)
            count += list[0]
            if list[0] > 0:
                for url in list[1]:
                    if url not in urls:
                        urls.append(url)
    except IOError:
        print("file not found")
    except:
        print("There was a generic error")
    return urls

def find_url(string):
    count, url, array = 0, '', []
    index = string.find('https://www.youtube.com/watch?v=')
    url = string[index+32:index+43]
    if index >= 0:
        count += 1
        array.append(url)
        find_url(string[index+43:])
    return count, array

def process_url(i, q, working, processed, failed):
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

def process_urls(working, processed, failed):
    for i in range(fetch_threads):
        worker = Thread(target=process_url, args=(i, enclosure_queue, working, processed, failed))
        worker.setDaemon(True)
        worker.start()
        enclosure_queue.join()

if __name__ == '__main__':
    main()


