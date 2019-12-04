from . import *
from .motley import *
from .spotify import *

import subprocess
import youtube_dl
from dataclasses import field
from abc import ABC

"""""



"""""

log = setup_logger(__name__)


@dataclass
class VideoFactory:
    url: str
    info_dict: dict = field(default_factory=dict)
    duration: int = None
    title: str = None
    description: str = None
    options: dict = youtube_options

    def __post_init__(self):
        self.get_info_dict()
        self.expand_info_dict()
        self.classify()

    def get_info_dict(self) -> None:
        with youtube_dl.YoutubeDL(self.options) as ydl:
            try:
                self.info_dict = ydl.extract_info(self.url, download=False)
                log.debug("Populated metadata for {} succesfully.".format(self.url))
                # TODO make the error handling here better
            except:
                log.error("Populating metadata for {} failed".format(self.url))
                raise Exception

    def expand_info_dict(self):
        self.duration = self.info_dict.get("duration")
        self.description = self.info_dict.get("description")
        self.title = self.info_dict.get("title")

    def classify(self):
        if self.description is not None:
            timestamps = self.countmatches(r"[0-9][0-9]\:[0-9][0-9]")
            if self.duration > 1200 or timestamps >= 5:
                return self.to_playlist()
            else:
                return self.to_song()
        else:
            return

    def to_song(self):
        return YoutubeSong(self.url, self.info_dict, self.name, None)

    def to_playlist(self):
        return YoutubePlaylist(self.url, self.info_dict)

    def to_audiobook(self):
        return YoutubeAudiobook(self.url, self.info_dict)

    def to_album(self):
        return YoutubeAlbum(self.url, self.info_dict)

    def to_other(self):
        return YoutubeOther(self.url, self.info_dict)


@dataclass
class Youtube(ABC):
    """"This is an abstract class, and only contains methods to be inherited"""
    url: str
    info_dict: dict = field(default_factory=dict)
    duration: int = None
    title: str = None
    description: str = None
    options: dict = youtube_options
    sp: Spotify = Spotify()

    def download(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.url])

    def hook(self, d):
        if d['status'] == 'finished':
            self.process()

    def process(self):
        raise TypeError("process cannot be run from base class, override the method")

    def push_to_db(self):
        raise TypeError("process cannot be run from base class, override the method")


@dataclass
class YoutubeSong(Youtube):
    song_name: str = None
    artist_name: str = None
    album_name: str = None

    def log(self):
        log.debug("Type: %s" % type(self).__name__)
        log.debug("URL : %s" % self.url)

    def populate_metadata(self):
        self.found = self.spotify.process()
        self.song_id, self.artist_id = self.spotify.return_song_artist()

    def hook(self, d):
        """Method override is only temporary, this should be removed in future, but keeps it working for now"""
        if d['status'] == 'finished':
            self.raw_filename = d['filename']
            self.convert()

    def edit_tags(self, file_path):
        tag_file = eyed3.load(file_path)
        tag_file.tag.artist = self.artist
        tag_file.tag.title = self.title
        tag_file.tag.album = self.album # needs matching
        tag_file.tag.save()

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

    def assign_metadata(self):
        """
        This would be better using a with statement, which would close the file automatically not explicitly.
        However doing this seems to result in an error, come back to this one later

        At the moment this only assigns the artwork for files.
        """
        eyed3file = eyed3.load(self.filename)
        image = open(artwork, "rb")
        imagestream = image.read()
        eyed3file.tag.images.set(3, imagestream, "image/jpeg")
        eyed3file.tag.save()
        image.close()

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

    def write_out(self):
        if alchemy.database_connected:
            self.push_to_db()
        else:
            self.push_to_file()

    def push_to_db(self):
        log.debug("Writing song to database: %s" %id(self))
        song = alchemy.Song()
        if self.playlist is not None:
            song.playlist_id = self.playlist.pk
        else:
            song.playlist_id = None
        song.title = self.name
        song.artist = self.artist
        song.url = self.url
        song.found = self.found
        song.artist_id = self.artist_id
        song.song_id = self.song_id
        song.user_id = "1" # Hardcoding this foreign key for the timebeing
        s = alchemy.session()
        s.add(song)
        s.commit()


class YoutubePlaylist(Youtube):
    def __init__(self, url, info_dict):
        super().__init__(url, info_dict)
        __tablename__ = "Playlists"
        self.type = "Playlist"
        """Attributes specific to playlists"""
        self.timestamps = []
        self.url = url
        self.num_songs = None
        self.find_timestamps()
        self.songs = []
        self.pk = None
        self.downloaded = False

    def log(self):
        log.debug("Type: %s" % type(self).__name__)
        log.debug("URL : %s" % self.url)

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

    def write_out(self):
        if alchemy.database_connected:
            self.push_to_db()
        else:
            self.push_to_file()

    def push_to_file(self):
        raise NotImplementedError

    def push_to_db(self):
        playlist = alchemy.Playlist()
        playlist.songs = self.songs
        playlist.url = self.url
        playlist.user_id = "1" # Hardcoding the foreign key for the timebeing
        playlist.song_count = self.num_songs
        playlist.title = self.name
        s = alchemy.session()
        s.add(playlist)
        s.commit()
        s.refresh(playlist) # is this neccessary?
        self.pk = playlist.id
        for song in self.songs:
            song.playlist_id = self.pk
            song.push_to_db()

    def download(self):
        try:
            with youtube_dl.YoutubeDL(self.options) as ydl:
                ydl.download([self.url])
        except:
            log.warning("Playlist at {} could not be downloaded.".format(id(self)))


class YoutubeAudiobook(Youtube):
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)
        self.type = "Audiobook"

    def process(self):
        raise NotImplementedError


class YoutubeAlbum(YoutubePlaylist):
    """This should explicitly search spotify for the album, different to playlist"""
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)
        self.type = "Album"

    def process(self):
        raise NotImplementedError


class YoutubeOther(Youtube):
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)
        self.type = "Other"

    def process(self):
        raise NotImplementedError


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=qoo27n_MPjY"
    runner = VideoFactory(url).classify()
    #print(runner.timestamps)
