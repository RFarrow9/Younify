from . import setup_logger
from .motley import singleton
from .spotify import *

from dataclasses import dataclass
"""""
A single pipeline object is the holder for all the main methods. This has the run, clear, queues etc.

This also instantiates the spotify connection.

"""""

log = setup_logger(__name__)

@singleton
@dataclass
class Pipe:
    spotify: Spotify = Spotify


if __name__ == "__main__":
    pipe = Pipe
