from younify import interface, frames, motley
import json
import logging
import sys

with open('c:\\config\\config.json') as f:
    config = json.load(f)

bookmarks = config["testing"]["bookmarks"]
logloc = config['logging']['path']


"""
This is the entry point for the program

"""


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


if __name__ == "__main__":
    setup_logger(__name__)
    run = Entry()