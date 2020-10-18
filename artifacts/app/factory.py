from spotify import *

import subprocess
import youtube_dl
from typing import Dict, List
from dataclasses import field
from abc import ABC
import re
import os

"""""
This class has the VideoFactory, and various types of videos in Youtube. The video app is used to designate the type of object
for the rest of program. This will pull down a dictionary of metadata of the video (length, title, description etc) which can be
used in order to designate the object.

At the moment this designation is done purely on duration, but in future it should be possible to generate a simple machine learning 
model using xgboost that can classify videos with high accuracy.

These are either; songs, playlists, albums, audiobook or other.

These all inherit from the Abstract base class of videos.

"""""

log = setup_logger(__name__)


@dataclass
class VideoFactory:
    url: str
    info_dict: Dict = field(default_factory=dict)
    duration: int = None
    title: str = None
    description: str = None
    options: Dict = field(default_factory=dict)
    error: bool = False

    def __post_init__(self):
        self.get_info_dict()
        self.expand_info_dict()

    def assign_defaults(self):
        self.options = youtube_options

    def get_info_dict(self) -> None:
        with youtube_dl.YoutubeDL(self.options) as ydl:
            try:
                self.info_dict = ydl.extract_info(self.url, download=False)
                log.debug("Populated metadata for {} successfully.".format(self.url))
                # TODO make the error handling here better
            except:
                log.error("Populating metadata for {} failed".format(self.url))
                self.error = True

    def expand_info_dict(self):
        self.duration = self.info_dict.get("duration")
        self.description = self.info_dict.get("description")
        self.title = self.info_dict.get("title")

    def classify(self):
        if not self.error:
            if self.description is not None:
                timestamps = self.countmatches(r"[0-9][0-9]\:[0-9][0-9]")
                if self.duration > 1200 or timestamps >= 5:
                    log.info(f"Video classified as playlist.")
                    return self.to_playlist()
                else:
                    log.info(f"Video classified as song")
                    return self.to_song()
            else:
                return

    def countmatches(self, pattern):
        if self.description is None:
            log.warning("No description information found for %s" % id(self))
            pass
        else:
            return re.subn(pattern, '', self.description)[1]

    def to_song(self):
        return YoutubeSong(url=self.url, info_dict=self.info_dict)

    def to_playlist(self):
        return YoutubePlaylist(url=self.url, info_dict=self.info_dict)

    def to_audiobook(self):
        return YoutubeAudiobook(self.url, self.info_dict)

    def to_album(self):
        return YoutubeAlbum(self.url, self.info_dict)

    def to_other(self):
        return YoutubeOther(self.url, self.info_dict)


@dataclass
class YoutubeVideos(ABC):
    """"This is an abstract class, and only contains methods to be inherited"""
    url: str
    info_dict: Dict = field(default_factory=dict)
    duration: int = None
    title: str = None
    description: str = None
    options: Dict = field(default_factory=dict)
    sp: Spotify = Spotify()
    type: str = None
    cache: CacheLayer = CacheLayer()

    def __post_init__(self):
        self.expand_info_dict()
        self.assign_defaults()

    @property
    def serialised(self):
        return f"\"{self.url}\",\"{self.type}\",\"{self.duration}\",\"{self.title}\",\"{self.description}\"\n"

    def expand_info_dict(self):
        self.duration = self.info_dict.get("duration")
        self.description = self.info_dict.get("description").replace("\n", " ").replace("\r", "").replace("\"", "\"\" ")
        self.title = self.info_dict.get("title").replace("\"", "\"\" ")

    def assign_defaults(self):
        self.options = youtube_options

    def download(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.url])

    def hook(self, d):
        if d['status'] == 'finished':
            self.process()

    def match_to_spotify(self):
        raise TypeError("process cannot be run from base class, override the method")

    def push_to_db(self):
        raise TypeError("process cannot be run from base class, override the method")



@dataclass
class YoutubeSong(YoutubeVideos):
    """
    1. Find the artist from the title of the video


    """
    type: str = "Song"
    song_name: str = None
    artist_name: str = None
    album_name: str = None

    def __post_init__(self):
        log.debug(f"Instantiated song object.")
        #self.info_dict()

    def main(self):
        self.populate_metadata()

    def log(self):
        log.debug("Type: %s" % type(self).__name__)
        log.debug("URL : %s" % self.url)

    def populate_metadata(self):
        self.found = self.sp.process()
        self.song_id, self.artist_id = self.spotify.return_song_artist()

    def hook(self, d):
        """Method override is only temporary, this should be removed in future, but keeps it working for now"""
        if d['status'] == 'finished':
            self.raw_filename = d['filename']
            self.convert()

    def convert(self):
            if self.raw_filename[-4:] == "webm":
                self.filename = self.raw_filename[0:-5] + ".mp3"
            else:
                self.filename = self.raw_filename[0:-4] + ".mp3"
            result = subprocess.run(
                ["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-i", self.raw_filename, "-acodec", "libmp3lame",
                 "-ab",
                 "128k", self.filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stderr:
                log.error(result.stderr)
            # filename = os.path.splitext(filename)[0]
            if self.artist is not None or self.title is not None:
                self.edit_tags(self.filename)
            self.assign_metadata()
            try:
                os.remove(self.raw_filename)
            except Exception as e:
                raise e

    def process(self):
        self.success = self.spotify.process()
        if not self.success:
            if self.url is not None:
                try:
                    self.download()
                except:
                    log.warning("Song %s failed to download." % self.name)
            elif self.playlist is not None:
                if not self.playlist.downloaded:
                    self.playlist.download()
                else:
                    raise NotImplemented #Needs to cut the playlist here for this particular song (if possible)

            else:
                log.critical("This object {} should not exist.".format(id(self)))
                self.log()

                # Handle failed and from playlist here
                # Should be pushed back up to playlist object?
        # automatically pushed to playlist if success already
        self.write_out()

    def match_to_spotify(self):
        self.identify_artist()
        artist_from_cache = self.cache.get_artist(self.artist_name)
        if artist_from_cache is None:
            potential_songs = self.sp.get_artist_songs()
            self.cache.put_artist(potential_songs)
        else:
            potential_songs = artist_from_cache[songs]
        #now we have the list
        # levenshtein check against each entry? But what are we checking?



        # 1. Try identify the artist from the title
        # 2. Try identify the artist from the description
        # 3.

    def identify_artist(self) -> None:
        pass

@dataclass
class YoutubePlaylist(YoutubeVideos):
    type: str = "Playlist"
    timestamps: list = field(default_factory=list)
    downloaded: bool = False

    def __post_init__(self):
        log.debug(f"Instantiated playlist object.")
        self.get_timestamps()
        self.expand_info_dict()

    @property
    def num_songs(self):
        return len(self.timestamps + 1)

    def get_timestamps(self):
        """This breaks apart the playlist into its timestamps"""
        pass

    def find_timestamps(self):
        """""
        This should find all the timestamps in the self.description and the song names.
        This will populate the num_songs and timestamps attributes.
        This should handle all known cases.
        """""
        desc_temp = ""
        regex_layer1 = r"[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]"
        regex_layer2 = r"[0-9]\:[0-9][0-9]"
        if self.timestamp_helper() == 2:
            log.debug("Description for object {} was found to have 2 timestamps per line".format(id(self)))
            for line in self.description.splitlines():
                if len(re.split(regex_layer2, line)) == 2:
                    print(line)
                if len(re.split(regex_layer2, line)) == 3:
                    print("in here")
                    splitline = re.split(regex_layer2, line)
                    line_mod = splitline[0]#.join(splitline[1])
                    desc_temp += line_mod + "\n"
                else:
                    desc_temp += line + "\n"
            self.description = desc_temp
        elif self.timestamp_helper() > 2:
            log.error("Description for object {} was found to have more than 2 timestamps per line".format(id(self)))
            raise NotImplemented
        self.num_songs = self.countmatches(regex_layer2)  # Counts the number of timestamps in the description, these dont overlap so this should work
        timestamps_layer1 = re.findall(regex_layer1, self.description)
        augmented_description = re.sub(regex_layer1, '', self.description)
        timestamps_layer2 = re.findall(regex_layer2, augmented_description)
        timestamps = timestamps_layer2 + timestamps_layer1
        for timestamp in timestamps:
            for line in self.description.splitlines():
                if timestamp in line:
                    self.timestamps.append([line.replace(timestamp, ""), timestamp])
                    break

    def timestamp_helper(self):
        """""
        This returns the average number of timestamps per line that has a timestamp.
        In a few cases, this has a value significantly above 1, in these examples it appears
        that the description meta has two timestamps per song (a finish and an end)
        """""
        countlines = 1
        countregexes = 0
        regex_layer = r"[0-9][0-9]\:[0-9][0-9]"
        for line in self.description.splitlines():
            if len(re.findall(regex_layer, line)) >= 1:
                ls = re.findall(regex_layer, line)
                countregexes += len(ls)
                countlines += 1
        return round(countregexes/countlines)

    def __str__(self):
        log.debug("--Youtube Playlist Instantiated")
        log.debug("URL: {}".format(self.url))
        log.debug("Songs in playlist: {}".format(str(self.num_songs)))

    def process(self):
        self.write_out()
        failure = 0
        for song in self.timestamps:
            log.debug("Instantiating YoutubeSong object for {}".format(str(song)))
            self.songs.append(YoutubeSong(url=None, info_dict=None, name=song[0], playlist=self))
        for obj in self.songs:
            obj.process()
            if not obj.success:
                failure = 1
        if failure == 1:
            self.download()
            self.cut()

    def hook(self, d):
        """Method override is only temporary, this should be removed in future, but keeps it working for now"""
        if d['status'] == 'finished':
            self.convert(d['filename'])

    def convert(self, filename):
        """"Add ref to self in here"""
        if filename[-4:] == "webm":
            processed_file_path = filename[0:-5] + ".mp3"
        else:
            processed_file_path = filename[0:-4] + ".mp3"
        result = subprocess.run(["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-i", filename, "-acodec", "libmp3lame", "-ab",
             "128k", processed_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stderr:
            log.error(result.stderr)
        try:
            os.remove(filename)
        except Exception as e:
            raise e

    def cut(self):
        raise NotImplementedError

    def push_to_file(self):
        raise NotImplementedError

    def download(self):
        try:
            with youtube_dl.YoutubeDL(self.options) as ydl:
                ydl.download([self.url])
        except:
            log.warning("Playlist at {} could not be downloaded.".format(id(self)))

    def expand_playlist_to_songs(self) -> List[YoutubeSong]:
        pass


@dataclass
class YoutubeAudiobook(YoutubeVideos):
    def __init__(self, url, info_dict):
        YoutubeVideos.__init__(self, url, info_dict)
        self.type = "Audiobook"

    def process(self):
        raise NotImplementedError


@dataclass
class YoutubeAlbum(YoutubePlaylist):
    """This should explicitly search spotify for the album, different to playlist"""
    def __init__(self, url, info_dict):
        YoutubeVideos.__init__(self, url, info_dict)
        self.type = "Album"

    def process(self):
        raise NotImplementedError


@dataclass
class YoutubeOther(YoutubeVideos):
    def __init__(self, url, info_dict):
        YoutubeVideos.__init__(self, url, info_dict)
        self.type = "Other"

    def process(self):
        raise NotImplementedError


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=qoo27n_MPjY"
    runner = VideoFactory(url).classify()
    #print(runner.timestamps)
