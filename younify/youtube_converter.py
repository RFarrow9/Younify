from younify import spotify, alchemy
import subprocess
import youtube_dl
import os
import re
import eyed3
import json
from abc import ABC

"""
This is the VideoFactory and URL class handling file
To use this correctly you will need to instantiate a instance of the VideoFactory
with a URL, call the method classify into another variable, for example (from external module):

    video = youtube_converter.VideoFactory("https://www.youtube.com/watch?v=" + url).classify()

Regardless of the classtype instantiated, they all then have the method process()

    video.process()

This will handle playlists/albums/songs/audiobooks accordingly

There are two kinds of playlist! single video ones (that we handle), and youtube based ones. 
"""

Base = alchemy.Base

with open('c:\\config\\config.json') as f:
    config = json.l(f)

root_dir = config["youtube_converter"]["root_dir"]
spotify_dir = config["youtube_converter"]["spotify_dir"]
artwork = config["youtube_converter"]["artwork"]


class VideoFactory:
    def __init__(self, url):
        self.url = url
        self.info_dict = None
        self.duration = None
        self.description = None
        self.options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'outtmpl': spotify_dir + '\%(title)s.%(ext)s',
            'quiet': True
        }
        self.populate()

    def populate(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            self.info_dict = info_dict
            self.duration = info_dict.get("duration")
            self.description = info_dict.get("description")

    def classify(self):
        """This is where we define what the video actually is"""
        #For now, we treat everything like a song
        if self.duration > 600:
            return self.to_playlist()
        elif self.duration <= 600:
            return self.to_song()

    def descriptionreader(self):
        #how do we pull out information from the description???
        print("placeholder")

    def to_song(self):
        return YoutubeSong(self.url, self.info_dict)

    def to_playlist(self):
        return YoutubePlaylist(self.url, self.info_dict)

    def to_audiobook(self):
        return YoutubeAudiobook(self.url, self.info_dict)

    def to_album(self):
        return YoutubeAlbum(self.url, self.info_dict)

    def to_other(self):
        return YoutubeOther(self.url, self.info_dict)


class Youtube(ABC):
    """"This is an abstract class, and only contains methods to be inherited"""
    def __init__(self, url, info_dict):
        self.url = url
        self.info_dict = info_dict
        self.options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'progress_hooks': [self.hook],
            'outtmpl': spotify_dir + '\%(title)s.%(ext)s',
            'quiet': True
        }
        self.name = None
        self.description = None
        self.id = None
        self.uploader = None
        self.thumbnail = None
        self.duration = None
        self.yt_track = None
        self.yt_artist = None
        if self.info_dict is not None:
            self.name = self.info_dict.get("title")
            self.description = self.info_dict.get("description")
            self.id = self.info_dict.get("id")
            self.uploader = self.info_dict.get("uploader")
            self.thumbnail = self.info_dict.get("thumbnail")
            self.duration = self.info_dict.get("duration")
            self.yt_track = self.info_dict.get("track")
            self.yt_artist = self.info_dict.get("artist")

    def __str__(self):
        return "type: " + type(self).__name__ + "\n" + "url: " + self.url

    def print_dict(self):
        print(self.info_dict)

    def print_desc(self):
        print(self.description)

    def download(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.url])

    def hook(self, d):
        if d['status'] == 'finished':
            self.process()

    def process(self):
        #if cls is Youtube:
        raise TypeError("process cannot be run from base class, override the method")
        #return object.__new__(cls, *args, **kwargs)


class YoutubeSong(Youtube):
    def __init__(self, url, info_dict, name, playlist=None):
        super().__init__(url, info_dict)
        if name is not None:
            self.name = name
        self.spotify = spotify.SpotifyMatching(self.name)
        self.success = None
        self.filename = None
        self.temp_filename = None
        """Attributes specific to songs"""
        self.found = None
        self.song_id = None
        self.artist_id = None
        self.artist = None
        self.title = None
        self.playlist = playlist

    def populate_metadata(self):
        self.found = self.spotify.process()
        self.song_id, self.artist_id = self.spotify.return_song_artist()

    def hook(self, d):
        """Method override is only temporary, this should be removed in future, but keeps it working for now"""
        if d['status'] == 'finished':
            self.temp_filename = d['filename']
            self.convert()

    def edit_tags(self, file_path):
        tag_file = eyed3.load(file_path)
        tag_file.tag.artist = self.artist
        tag_file.tag.title = self.title
        tag_file.tag.album = self.album # needs matching
        tag_file.tag.save()

    def convert(self):
            if self.temp_filename[-4:] == "webm":
                self.filename = self.temp_filename[0:-5] + ".mp3"
            else:
                self.filename = self.temp_filename[0:-4] + ".mp3"
            result = subprocess.run(
                ["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-i", self.temp_filename, "-acodec", "libmp3lame",
                 "-ab",
                 "128k", self.filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stderr:
                print(result.stderr)
            # filename = os.path.splitext(filename)[0]
            if self.artist is not None or self.title is not None:
                self.edit_tags(self.filename)
            self.assign_metadata()
            # try:
            #    os.rename(processed_file_path, processed_file_path)
            # except Exception as e:
            #    os.remove(filename)
            #    os.remove(processed_file_path)
            #    raise e
            try:
                os.remove(self.temp_filename)
            except Exception as e:
                raise e

    def assign_metadata(self):
        """
        This would be better usign a with statement, which would close the file automatically not explicitly.
        However doing this seems to result in an error, come back to this later

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
                self.download()
            else:
                print("placeholder")
                # Handle failed and from playlist here
                # Should be pushed back up to playlist object?
        # automatically pushed to playlist if success already
        self.push_to_db()

    def push_to_db(self):
        song = alchemy.Song()
        song.playlist_id = self.playlist.id
        song.title = self.name
        song.artist = self.artist
        song.url = self.url
        song.found = self.found
        song.artist_id = self.artist_id
        song.song_id = self.song_id
        song.user_id = "1" # Hardcoding the foreign key for the timebeing
        s = alchemy.session()
        s.add(song)
        s.commit()


class YoutubePlaylist(Youtube):
    """This should treat each song in the playlist like a YoutubeSong object
        How do we specify that a video that is part of a playlist is handled like a
        song/playlist?
    """
    def __init__(self, url, info_dict):
        super().__init__(url, info_dict)
        __tablename__ = "Playlists"
        """Attributes specific to playlists"""
        self.timestamps = []
        self.url = url
        self.num_songs = None
        self.find_timestamps()
        # This should hold the objects that represent YoutubeSongs
        self.songs = []
        self.playlist_pk = None

    def find_timestamps(self):
        regex_layer1 = r"[0-9]\:[0-9][0-9]\:[0-9][0-9]"
        regex_layer2 = r"[0-9][0-9]\:[0-9][0-9]"
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

    def __str__(self):
        return "type: " + type(self).__name__ + "\n" + "url: " + self.url + "\n" + "songs in playlist: " + str(self.num_songs)

    def process(self):
        failure = 0
        for song in self.timestamps:
            self.songs.append(YoutubeSong(url=None, info_dict=None, name=song[0], playlist=self))
        for obj in self.songs:
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
        result = subprocess.run(
            ["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-i", filename, "-acodec", "libmp3lame",
             "-ab",
             "128k", processed_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stderr:
            print(result.stderr)
        try:
            os.remove(filename)
        except Exception as e:
            raise e

    def countmatches(self, pattern):
        return re.subn(pattern, '', self.description)[1]

    def cut(self):
        print("placeholder")

    def push_to_db(self):
        playlist = alchemy.Playlist()
        playlist.songs = self.songs
        playlist.url = self.url
        playlist.user_id = "1" # Hardcoding the foreign key for the timebeing
        s = alchemy.session()
        s.add(playlist)
        s.commit()
        self.playlist_pk = s.query(alchemy.Playlist).filter(alchemy.Playlist.url == self.url).one().pk
        for song in self.songs:
            song.playlist_id = self.playlist_pk
            song.push_to_db()


class YoutubeAudiobook(Youtube):
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)

    def process(self):
        print("placeholder")


class YoutubeAlbum(Youtube):
    """This should explicitly search spotify for the album, different to playlist"""
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)

    def process(self):
        print("placeholder")


class YoutubeOther(Youtube):
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)

    def process(self):
        print("placeholder")


if __name__ == "__main__":
    print("nothing to do here")

