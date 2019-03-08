import subprocess
import youtube_dl
from younify import spotify
import os
import eyed3
import json

with open('c:\\config\\config.json') as f:
    config = json.load(f)

root_dir = config["youtube_converter"]["root_dir"]
spotify_dir = config["youtube_converter"]["spotify_dir"]

class Classifier:
    def __init__(self, url):
        self.url = url
        self.id = None
        self.name = None
        self.description = None
        self.info_dict = None
        self.options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'outtmpl': spotify_dir + '\%(title)s.%(ext)s'
        }
        self.populate()

    def populate(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            self.info_dict = info_dict.get("id", None)
            self.name = info_dict.get("title")
            self.description = info_dict.get("description")
            self.id =
            self.uploader =
            self.thumbnail =
            self.duration =
            self.yt_track =
            self.yt_artist =

    def factory(self):
        if self.duration > 600:
            return self.tosong()
        elif self.duration <= 600:
            return self.tosong()

    def tosong(self):




class YoutubeSong:
    def __init__(self, url, artist=None, title=None): #should the download be tied to init?
        self.artist = artist
        self.title = title
        self.url = url
        self.info_dict = None
        self.options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'progress_hooks': [self.hook],
            'outtmpl': spotify_dir + '\%(title)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(self.options) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            self.info_dict = info_dict
            self.id = info_dict.get("id", None)
            self.name = info_dict.get("title")
            self.spotify = spotify.SpotifyMatching(self.name)

    def download(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.url])

    def print_dict(self):
        print(self.info_dict)

    def print(self):
        print("Video Title: " + str(self.name))
        print("Video ID: " + str(self.id))

    def hook(self, d):
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

class YoutubePlaylist:
    def __init__(self):
        #do stuff

    def process(self):
        #this bit should be polymorphic so it is processed like all the others

class YoutubeAudiobook:
    def __init__(self):
        #do different stuff

    def process(self):
        #polymorphic part

class YoutubeAlbum:
    def __init__(self):
        # do stuff

    def process(self):
        # this bit should be polymorphic so it is processed like all the others

class YoutubeOther:
    def __init__(self):
        #do stuff

    def process(self):
        #do we want to process these?


def main():
    #Url(['https://www.youtube.com/watch?v=RPxvTd_jCPQ'], "Young Scrolls", "Sheogorath - Zoom")
    #get_audio(["https://www.youtube.com/watch?v=xdOykEJSXIg"], "Anthony Hamilton", "Freedom")
    print(root_dir)

if __name__ == "__main__":
    #print("nothing to do here")
    main()
