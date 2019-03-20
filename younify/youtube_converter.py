import subprocess
import youtube_dl
from younify import spotify
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

"""

with open('c:\\config\\config.json') as f:
    config = json.load(f)

root_dir = config["youtube_converter"]["root_dir"]
spotify_dir = config["youtube_converter"]["spotify_dir"]


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
        if cls is Youtube:
            raise TypeError("process cannot be run from base class, override the method")
        return object.__new__(cls, *args, **kwargs)

class YoutubeSong(Youtube):
    def __init__(self, url, info_dict): #should the download be tied to init?
        super().__init__(url, info_dict)
        self.spotify = spotify.SpotifyMatching(self.name)
        self.success = None
        """Attributes specific to songs"""
        self.found = None
        self.song_id = None
        self.artist_id = None
        self.artist = None
        self.title = None

    def populate_metadata(self):
        self.found = self.spotify.process()
        self.song_id, self.artist_id = self.spotify.return_song_artist()

    def hook(self, d):
        """Method override is only temporary, this should be removed in future, but keeps it working for now"""
        if d['status'] == 'finished':
            self.filename = d['filename']
            self.convert()

    def edit_tags(self, file_path):
        tag_file = eyed3.load(file_path)
        tag_file.tag.artist = self.artist
        tag_file.tag.title = self.title
        tag_file.tag.album = self.title
        tag_file.tag.save()

    def convert(self):
            if filename[-4:] == "webm":
                processed_file_path = self.filename[0:-5] + ".mp3"
            else:
                processed_file_path = self.filename[0:-4] + ".mp3"
            result = subprocess.run(
                ["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-i", filename, "-acodec", "libmp3lame",
                 "-ab",
                 "128k", processed_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stderr:
                print(result.stderr)
            #filename = os.path.splitext(filename)[0]
            if self.artist is not None or self.title is not None:
                self.edit_tags(processed_file_path)
            #try:
            #    os.rename(processed_file_path, processed_file_path)
            #except Exception as e:
            #    os.remove(filename)
            #    os.remove(processed_file_path)
            #    raise e
            try:
                os.remove(filename)
            except Exception as e:
                raise e

    def assign_metadata(self):


    def process(self):
        self.success = self.spotify.process()
        if not self.success:
            self.download()
            #automatically calls the conversion and follows through

class YoutubePlaylist(Youtube):
    """This should treat each song in the playlist like a YoutubeSong object"""
    def __init__(self, url, info_dict):
        super().__init__(url, info_dict)
        """Attributes specific to playlists"""
        self.timestamps = [,]
        regex_layer1 = r"[0-9]\:[0-9][0-9]\:[0-9][0-9]"
        regex_layer2 = r"[0-9][0-9]\:[0-9][0-9]"
        self.num_songs = self.countmatches(regex_layer2) #Counts the number of timestamps in the description, these dont overlap so this should work
        timestamps_layer1 = re.findall(regex_layer1, self.description)
        augmented_description = re.sub(regex_layer1, '', self.description)
        timestamps_layer2 = re.findall(regex_layer2, augmented_description)
        timestamps = timestamps_layer2 + timestamps_layer1
        for timestamp in timestamps:
           for line in self.description:
               if timestamp in line:
                   self.timestamps.append(line.replace(timestamp, ""), timestamp)
                   break
                   break
        for item in self.timestamps:
            print(item)
           #    matchObj = re.match(regex, self.description)
   #     for i in range(self.num_songs-2):
    #        self.temp += matchObj.group(i+1) #at the moment grab the info into a single variable
        #If this is null, can we grab the top 10 comments for example and do it with this?

    def __str__(self):
        return "type: " + type(self).__name__ + "\n" + "url: " + self.url + "\n" + "songs in playlist: " + str(self.num_songs)

    def process(self):
        self.download()
    #    self.cut()
    #    for each song in playlist:
    #        video = VideoFactory("filename" as file).classify()
    #    print("placeholder")

    def hook(self, d):
        """Method override is only temporary, this should be removed in future, but keeps it working for now"""
        if d['status'] == 'finished':
            self.convert(d['filename'])

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
        # filename = os.path.splitext(filename)[0]
        #if self.artist is not None or self.title is not None:
        #    self.edit_tags(processed_file_path)
        # try:
        #    os.rename(processed_file_path, processed_file_path)
        # except Exception as e:
        #    os.remove(filename)
        #    os.remove(processed_file_path)
        #    raise e
        try:
            os.remove(filename)
        except Exception as e:
            raise e

    def countmatches(self, pattern):
        return re.subn(pattern, '', self.description)[1]

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
