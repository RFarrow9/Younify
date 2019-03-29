import eyed3
from younify import spotify

"""Behaviour: Take from the file the name/artist/album whatever metadata can be scraped and use this to find the song in spotify
At this point in time there are no fancy factories/singletons/abstract base classes required due to limited functionality.
"""


class FileHandler:
    def __init__(self, file):
        self.file = file
        """Filename needs to exclude filetype"""
        self.filetags = eyed3.load(self.file)
        #Assumption here is that the filename can be treated the same as a youtube title string
        #Validate this assumption
        self.sp = spotify.SpotifyMatching(self.filename)

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
        return str(self.filename)
