from . import setup_logger
from .spotify import *
from .factory import YoutubeVideos, VideoFactory

from singleton_decorator import singleton
from typing import List, Tuple
from dataclasses import dataclass, field
"""""
A single pipeline object is the holder for all the main methods. This has the run, clear, queues etc.

This also instantiates the spotify connection.

"""""

log = setup_logger(__name__)


@singleton
@dataclass
class Pipe:
    spotify: Spotify = Spotify
    unclassified: List[str] = field(default_factory=list)
    classified: List[YoutubeVideos] = field(default_factory=list)
    errored: List[Tuple] = field(default_factory=tuple)
    complete: List[YoutubeVideos] = field(default_factory=list)

    def main(self):
        self.get_urls()
        self.classify_urls()

    def get_urls(self):
        self.unclassified.extend(["https://www.youtube.com/watch?v=hqbS7O9qIXE"])

    def classify_urls(self):
        for url in self.unclassified:
            self.classified.extend([VideoFactory(url).classify()])


if __name__ == "__main__":
    pipe = Pipe()
    pipe.main()
