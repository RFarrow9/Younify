import eyed3
import os
from datetime import date
from younify import spotify

"""
Behaviour: Take from the file the name/artist/album whatever metadata can be scraped and use this to find the song in spotify
At this point in time there are no fancy factories/singletons/abstract base classes required due to limited functionality.
"""


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
        print("placeholder")
        #self.filename = substring(self.file)

    def third_pass(self):
        """""For third pass we assume there is no valid metadata at all and use fingerprinting services"""
        #take 2 30 second clips, push to free fingerprinting services to identify information
        #parse the json file for information, then use this to find song in spotify

    def process(self):
        self.sp.process()

    def move_file(self):
        """"Move the file to specified location"""
        print("placeholder")

    def convert_file(self):
        """"Convert the file to standard format (mp3?) if not already"""
        print("placeholder")

    def __str__(self):
        return str(self.file)

    def __repr__(self):
        # how do?


class FolderHandler:
    # use os.path.join()
    def __init__(self, path):
        """"note that self.file references are local"""
        if path[:-1] == "\\":
            self.path = path[0:-1]
        else:
            self.path = path
        self.files = os.listdir(self.path)
        if "Thumbs.db" in self.files: self.files.remove("Thumbs.db")
        self.oldest = None
        self.newest = None

    def get_oldest_file(self):
        oldest_time = None
        oldest_file = None
        if len(self.files) == 0:
            print("no files in directory")
        else:
            oldest_file = self.files[0]
            oldest_time = os.path.getctime(self.path + '\\' + oldest_file)
        if len(self.files) >= 2:
            for file in self.files:
                file = self.path + "\\" + file
                if oldest_time > os.path.getctime(file):
                    oldest_time = os.path.getctime(file)
                    oldest_file = file
        self.oldest = oldest_file
        return FileHandler(self.oldest)

    def get_newest_file(self):
        newest_time = None
        newest_file = None
        if len(self.files) == 0:
            print("no files in directory")
        else:
            newest_file = self.files[0]
            newest_time = os.path.getctime(self.path + '\\' + newest_file)
        if len(self.files) >= 2:
            for file in self.files:
                file = self.path + '\\' + file
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
            os.rename(self.path + '\\' + file, newfolder + '\\' + archivedate + file)
        #Do not change path after operation, so now points to an empty dir