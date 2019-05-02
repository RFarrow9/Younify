import json

"""""
Purpose of this is to interface the fingerprinting apis with the rest of the program for a 
last ditch effort (third pass) at identifying songs correctly, either from file or from url.
"""


class FingerPrinter:
    def __init__(self, song):
        if song.filename is not None:
            print("placeholder")
        # check the file is already downloaded
        # if it is, then great we can work with this

    def __str__(self):
        return "checked against..."
