import subprocess
import youtube_dl
from younify import spotify
import os
import eyed3
import json
from abc import ABC

with open('c:\\config\\config.json') as f:
    config = json.load(f)

root_dir = config["youtube_converter"]["root_dir"]
spotify_dir = config["youtube_converter"]["spotify_dir"]

class Factory:
    def __init__(self, url):
        self.url = url
        self.info_dict = None
        self.duration = None
        self.options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'outtmpl': spotify_dir + '\%(title)s.%(ext)s'
        }
        self.populate()
        self.factory()

    def populate(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            self.info_dict = info_dict
            self.duration = info_dict.get("duration")

    def factory(self):
        """This is where we define what the video actually is"""
        #For now, we treat everything like a song
        if self.duration > 600:
            return self.to_song()
        elif self.duration <= 600:
            return self.to_song()

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
            'outtmpl': spotify_dir + '\%(title)s.%(ext)s'
        }
        self.name = self.info_dict.get("title")
        self.description = self.info_dict.get("description")
        self.id = self.info_dict.get("id")
        self.uploader = self.info_dict.get("uploader")
        self.thumbnail = self.info_dict.get("thumbnail")
        self.duration = self.info_dict.get("duration")
        self.yt_track = self.info_dict.get("track")
        self.yt_artist = self.info_dict.get("artist")

    def __str__(self):
        print(self.url)

    def print_dict(self):
        print(self.info_dict)

    def download(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.url])

    def hook(self, d):
        if d['status'] == 'finished':
            self.process()

    def process(self):
        print("shouldn't be here")

class YoutubeSong(Youtube):
    def __init__(self, url, info_dict): #should the download be tied to init?
        Youtube.__init__(self, url, info_dict)
        self.spotify = spotify.SpotifyMatching(self.name)

    def download(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.url])

    def hook(self, d):
        """Method override is only temporary, this should be removed in future, but keeps it working for now"""
        if d['status'] == 'finished':
            self.convert(d['filename'])

    def edit_tags(self, file_path):
        tag_file = eyed3.load(file_path)
        tag_file.tag.artist = self.artist
        tag_file.tag.title = self.title
        tag_file.tag.album = self.title
        tag_file.tag.save()

    def convert(self, filename):
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
            filename = os.path.splitext(filename)[0]
            if self.artist is not None or self.title is not None:
                self.edit_tags(processed_file_path)
            try:
                os.rename(processed_file_path, processed_file_path)
            except Exception as e:
                os.remove(filename)
                os.remove(processed_file_path)
                raise e
            try:
                os.remove(filename)
            except Exception as e:
                raise e

    def process(self):
        #polymorphic part

class YoutubePlaylist(Youtube):
    """This should treat each song in the playlist like a YoutubeSong object"""
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)

    def process(self):
        #this bit should be polymorphic so it is processed like all the others
        print("placeholder")

class YoutubeAudiobook(Youtube):
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)

    def process(self):
        print("placeholder")

class YoutubeAlbum(Youtube):
    """This should explicitly search spotify for the album, different to playlist!"""
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)

    def process(self):
        print("placeholder")

class YoutubeOther(Youtube):
    def __init__(self, url, info_dict):
        Youtube.__init__(self, url, info_dict)

    def process(self):
         print("placeholder")


def main():
    #Url(['https://www.youtube.com/watch?v=RPxvTd_jCPQ'], "Young Scrolls", "Sheogorath - Zoom")
    #get_audio(["https://www.youtube.com/watch?v=xdOykEJSXIg"], "Anthony Hamilton", "Freedom")
    print(root_dir)

if __name__ == "__main__":
    #print("nothing to do here")
    main()
