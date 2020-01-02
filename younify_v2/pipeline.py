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
limit = None

@singleton
@dataclass
class Pipe:
    spotify: Spotify = Spotify
    unclassified: List[str] = field(default_factory=list)
    classified: List[YoutubeVideos] = field(default_factory=list)
    errored: List[Tuple] = field(default_factory=tuple)
    complete: List[YoutubeVideos] = field(default_factory=list)

    def main(self):
        self.get_urls_from_file("./resources/output")
        self.classify_urls()
        self.serialise_objects("./resources/output_enriched.csv")
        self.match_to_spotify()

    def get_urls(self):
        self.unclassified.extend(["https://www.youtube.com/watch?v=hqbS7O9qIXE"])

    def get_urls_from_file(self, input):
        head = []
        if limit:
            with open(input, "r", encoding="utf-8") as file:
                head = [next(file) for x in range(limit)]
        else:
            with open(input, "r", encoding="utf-8") as file:
                for line in file:
                    head.extend([line])
        for url in head:
            self.unclassified.extend([f"https://www.youtube.com/watch?v={url[:-1]}"])

    def classify_urls(self):
        for url in self.unclassified:
            object = VideoFactory(url).classify()
            if object is not None:
                self.classified.extend([object])

    def serialise_objects(self, output):
        """Produces a csv output of all the classified urls"""
        with open(output, "w+", encoding="utf-8") as write_file:
            write_file.write("url, type, length, title, description")
            for url in self.classified:
                write_file.write(url.serialised)

    def match_to_spotify(self):
        for url in self.classified:
            url.match_to_spotify()


if __name__ == "__main__":
    pipe = Pipe()
    pipe.main()
