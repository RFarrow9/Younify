from younify import *
from datetime import date
import socket
import pathlib
import glob

"""
Behaviour: Take from the file the name/artist/album whatever metadata can be scraped and use this to find the song in spotify
At this point in time there are no fancy factories/singletons/abstract base classes required due to limited functionality.

The FileHandler is also used to handle files created y the youtube_converter process, so has write methods as well as read.
"""


def setup_logger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh = logging.FileHandler(logloc)
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        log.error("Internet connection severed. Pausing threads and retrying.: %s" %ex)
        for x in range(0, 20):
            try:
                socket.setdefaulttimeout(timeout)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
                return True
            except:
                pass
            time.sleep(10)
        log.critical("Internet connection severed. No active internet connection detected after 200 seconds.")
        return False


class FileHandler:
    def __init__(self, file):
        self.file = file
        """Filename needs to exclude filetype"""
        self.filetags = eyed3.load(self.file)
        #Assumption here is that the filename can be treated the same as a youtube title string
        #Validate this assumption
        self.sp = spotify.SpotifyMatching(self.file)

    def first_pass(self):
        """"for first pass we assume the file has valid metadata"""
        self.title = self.filetags.title
        self.artist = self.filetags.artist
        self.album = self.filetags.album

    def second_pass(self):
        """"for second pass we assume the only metadata is the filename itself"""
        raise NotImplemented()

    def third_pass(self):
        """""For third pass we assume there is no valid metadata at all and use fingerprinting services"""
        #take 2 30 second clips, push to free fingerprinting services to identify information
        #parse the json file for information, then use this to find song in spotify

    def process(self):
        self.sp.process()

    def move_file(self):
        """"Move the file to specified location"""
        raise NotImplemented()

    def convert_file(self):
        """"Convert the file to standard format (mp3?) if not already"""
        raise NotImplemented()

    def __str__(self):
        return str(self.file)

    def __repr__(self):
        raise NotImplemented()
        # how do?


class FolderHandler:
    def __init__(self, path):
        self.path = pathlib.WindowsPath(path)
        self.files = glob.glob(self.path / '*.*')
        if "Thumbs.db" in self.files:
            self.files.remove("Thumbs.db")
        self.oldest = None
        self.newest = None

    def get_oldest_file(self):
        oldest_time = None
        oldest_file = None
        if len(self.files) == 0:
            log.warning("No files found in directory: %s" % self.path)
        else:
            oldest_file = self.files[0]
            oldest_time = os.path.getctime(self.path / oldest_file)
        if len(self.files) >= 2:
            for file in self.files:
                file = self.path / file
                if oldest_time > os.path.getctime(file):
                    oldest_time = os.path.getctime(file)
                    oldest_file = file
        self.oldest = oldest_file
        return FileHandler(self.oldest)

    def get_newest_file(self):
        newest_time = None
        newest_file = None
        if len(self.files) == 0:
            log.warning("No files found in directory: %s" % self.path)
        else:
            newest_file = self.files[0]
            newest_time = os.path.getctime(self.path / newest_file)
        if len(self.files) >= 2:
            for file in self.files:
                file = self.path / file
                if newest_time < os.path.getctime(file):
                    newest_time = os.path.getctime(file)
                    newest_file = file
        self.newest = newest_file
        return FileHandler(self.newest)

    def move_all_files(self, newfolder, archive=True):
        if archive:
            archivedate = str(date.today())
        else:
            archivedate = ""
        for file in self.files:
            os.rename(self.path / file, newfolder / archivedate / file)


log = setup_logger(__name__)


def main():
    print("This is not the entry point. Either run unittests, or run entry.py")


if __name__ == '__main__':
    main()