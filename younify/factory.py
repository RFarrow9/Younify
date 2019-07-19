from younify import *
import subprocess
import youtube_dl
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


log = motley.setup_logger(__name__)


class VideoFactory:
    def __init__(self, url):
        log.debug("VideoFactory with URL of %s has been instantiated." % url)
        self.url = url
        self.info_dict = None
        self.duration = None
        self.name = None
        self.description = None
        self.options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'outtmpl': spotify_dir + '\%(title)s.%(ext)s',
            'quiet': True
        }
        try:
            log.debug("Populating metadata for %s." % url)
            self.populate()
        except:
            log.error("Populating metadata for %s has failed." % url)
            pass

    def __repr__(self):
        return self.url

    def populate(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            try:
                info_dict = ydl.extract_info(self.url, download=False)
            except:
                log.DEBUG("Populating metadata for %s." % self.url)
            self.info_dict = info_dict
            self.duration = info_dict.get("duration")
            self.description = info_dict.get("description")
            self.name = self.info_dict.get("title")

    def classify(self):
    # For now, we treat everything like a song or playlist
        if self.description is not None:
            timestamps = self.countmatches(r"[0-9][0-9]\:[0-9][0-9]")
            if self.duration > 1200 or timestamps >= 5:
                return self.to_playlist()
            else:
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
        return YoutubeSong(self.url, self.info_dict, self.name, None)

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
            'format': 'bestaudio/best',
            'extractaudio': True,
            'noplaylist': True,
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

    def countmatches(self, pattern):
        return re.subn(pattern, '', self.description)[1]

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


class YoutubeSong(Youtube):
    def __init__(self, url, info_dict, name, playlist=None):
        super().__init__(url, info_dict)
        if url is None: # Then is from playlist
            self.name = name
        else:
            self.name = self.info_dict.get("title")
        self.spotify = spotify.SpotifyMatching(self.name)
        self.success = None
        self.filename = None
        self.raw_filename = None
        self.type = "Song"
        """Attributes specific to songs"""
        self.found = None
        self.song_id = None
        self.artist_id = None
        self.artist = None
        self.title = None
        self.playlist = playlist

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
            else:
                log.debug("Spotify methods failing, will do manual downloads here.")
                # Handle failed and from playlist here
                # Should be pushed back up to playlist object?
        # automatically pushed to playlist if success already
        self.push_to_db()

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

    def log(self):
        log.debug("Type: %s" % type(self).__name__)
        log.debug("URL : %s" % self.url)

    def find_timestamps(self):
        regex_layer1 = r"[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]"
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
        log.debug("--Youtube Playlist Instantiated")
        log.debug("URL: {}".format(self.url))
        log.debug("Songs in playlist: {}".format(str(self.num_songs)))

    def process(self):
        self.push_to_db()
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
        result = subprocess.run(
            ["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-i", filename, "-acodec", "libmp3lame",
             "-ab",
             "128k", processed_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stderr:
            log.error(result.stderr)
        try:
            os.remove(filename)
        except Exception as e:
            raise e

    def cut(self):
        raise NotImplemented()

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


class YoutubeAudiobook(Youtube):
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)
        self.type = "Audiobook"

    def process(self):
        raise NotImplemented()


class YoutubeAlbum(YoutubePlaylist):
    """This should explicitly search spotify for the album, different to playlist"""
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)
        self.type = "Album"

    def process(self):
        raise NotImplemented()


class YoutubeOther(Youtube):
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)
        self.type = "Other"

    def process(self):
        raise NotImplemented()


