from younify import framework
import json

with open('c:\\config\\config.json') as f:
    config = json.load(f)

bookmarks = config["testing"]["bookmarks"]

class Entry:
    def __init__(self):
        self.setup_empty()
        self.WorkingURLs.push_file_to_working(bookmarks)
        self.WorkingURLs.update_temp()
        self.WorkingURLs.push_urls_to_queue()
        self.WorkingURLs.process_urls(self.ProcessedURLs)

    def setup_empty(self):
        self.WorkingURLs = framework.working
        self.FailedURLs = framework.failed
        self.ProcessedURLs = framework.processed
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()


if __name__ == "__main__":
    run = Entry()