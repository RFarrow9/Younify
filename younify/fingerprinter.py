import logging
from younify import motley

"""""
Purpose of this is to interface the fingerprinting apis with the rest of the program for a 
last ditch effort (third pass) at identifying songs correctly, either from file or from url.
"""


motley.setup_logger(__name__)
log = logging.getLogger(__name__)



class FingerPrinter:
    def __init__(self, file=motley.FileHandler):
        if file.name is not None:
            print("placeholder")
        # check the file is already downloaded
        # if it is, then great we can work with this

    def __str__(self):
        return "checked against..."
