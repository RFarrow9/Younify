from younify import *

"""
This is the entry point for the program

"""

log = motley.setup_logger(__name__)

class Entry:
    def __init__(self):
        self.setup_empty()
        self.WorkingURLs.push_file_to_working(bookmarks)
        self.WorkingURLs.update_temp()
        self.WorkingURLs.push_urls_to_queue()
        self.WorkingURLs.process_urls(self.ProcessedURLs)

    def setup_empty(self):
        self.WorkingURLs = frames.working
        self.FailedURLs = frames.failed
        self.ProcessedURLs = frames.processed
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()


def main():
    print("This is not the entry point. Either run unittests, or run entry.py")


if __name__ == '__main__':
    main()
