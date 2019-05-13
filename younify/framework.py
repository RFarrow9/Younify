import queue
import json
from threading import Thread
from younify import youtube_converter

"""
Should we be using 'processed' as an array, or only hold fails and working?
Processed could be sent to azure.
Push to local file in case of limited database availability/backup recovery?
Option to push to database? Is it neccessary?
Thread count should come from environment variable if available
Should the JSON interacter be in a seperate file? (as opposed to reinitialised per module)
Work out global access to these objects (singleton?)
"""

fetch_threads = 4
# use NUMBER_OF_PROCESSORS env var? This might work for windows, but what about unix?
enclosure_queue = queue.Queue()
# Convert these into JSON configs
with open('c:\\config\\config.json') as f:
    config = json.load(f)

temp_processing = config["framework"]["processing"]
temp_working = config["framework"]["working"]


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
            with open(temp_processing, "w+") as f:
                for line in f:
                    self.add_url("https://www.youtube.com/watch?v="+line[:-1])
        except:
            print("file not found or could classify video")

    def update_temp(self):
        file = open(temp_processing, "w+")
        for URL in self.urls:
            file.write(URL[-11:] + "\r")
        file.close()


class WorkingURLs(ProcessingArray):
    def __init__(self):
        ProcessingArray.__init__(self)
        try:
            with open(temp_working, "r") as f:
                for line in f:
                    self.add_url("https://www.youtube.com/watch?v="+line[:-1])
        except:
            print("file not found")

    def update_temp(self):
        file = open(temp_working, "w+")
        for URL in self.urls:
            file.write(URL[-11:] + "\r")
        file.close()

    def push_file_to_working(self, filename):
        array = find_urls_in_file(filename)
        for url in array:
            self.add_url(url)

    def push_url_to_queue(self, url):
        self.add_url(url)
        enclosure_queue.put(youtube_converter.VideoFactory(url).classify())
        # Object is only classified (expensive) when put into the queue! Not before.

    def push_urls_to_queue(self):
        if self.count_urls() > 0:
            for url in self.retrieve_urls():
                enclosure_queue.put(url)

    def __process_url(self, i, q, processed):
        while True:
            url = q.get()
            video = youtube_converter.VideoFactory("https://www.youtube.com/watch?v=" + url).classify()
            print(video)
            video.print_dict()
            video.download()
            processed.add_url(url)
            self.remove_url(url)
            q.task_done()

    def process_urls(self, processed):
        for i in range(fetch_threads):
            worker = Thread(target=self.__process_url, args=(i, enclosure_queue, processed))
            worker.setDaemon(True)
            worker.start()
            enclosure_queue.join()

    def process_url(self, url, processed):
        try:
            youtube_converter.get_audio("https://www.youtube.com/watch?v=" + url, "", "")
            processed.add_url(url)
        except:
            #add proper error handling here
            print("error unknown")
        finally:
            self.remove_url(url)


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


def linecount(filename):
    count = 0
    file = open(filename)
    for line in file:
        count += 1
    file.close()
    return count


def find_urls_in_file(filename):
    count, urls = 0, []
    file = open(filename, encoding='utf8')
    try:
        for line in file:
            urllist = find_url(line)
            count += urllist[0]
            if urllist[0] > 0:
                for url in urllist[1]:
                    if url not in urls:
                        urls.append(url)
    except IOError:
        print("file not found")
    except:
        print("There was a generic error")
    finally:
        file.close()
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


def main():
    print("Nothing to do here.")


def prime():
    # This is not the best way to do this, but at the moment allows for 'global access'
    global processed
    processed = ProcessedURLs()
    global working
    working = WorkingURLs()
    global failed
    failed = FailedURLs()


if __name__ == "__main__":
    main()
else:
    prime()



