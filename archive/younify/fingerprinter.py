from younify import *

"""""
Purpose of this is to interface the fingerprinting apis with the rest of the program for a 
last ditch effort (third pass) at identifying songs correctly, either from file or from url.
"""

log = motley.setup_logger(__name__)


class FingerPrinter:
    def __init__(self, file=motley.FileHandler):
        if file.name is not None:
            raise NotImplemented()
        raise NotImplemented()
        # check the file is already downloaded
        # if it is, then great we can work with this

    def __str__(self):
        raise NotImplemented()


def main():
    print("This is not the entry point. Either run unittests, or run entry.py")


if __name__ == '__main__':
    main()
