import subprocess
import youtube_dl
import os
import eyed3
import json


with open('config.json') as f:
    config = json.load(f)

root_dir = "C:\\Users\\robfa\\Documents\\Python\\Youtube Thing"
temp_dir = root_dir + "\\Temp"
spotify_dir = "C:\\Users\\robfa\\Music\\From YouTube"

class Url:
    def __init__(self, url, artist=None, title=None):
        self.artist = artist
        self.title = title

        root_dir = config["youtube_converter"]["root_dir"]
        temp_dir = root_dir + "\\Temp"

        options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'progress_hooks': [self.hook],
            'outtmpl': '%(title)s.%(ext)s'
        }
        os.chdir(temp_dir)
        with youtube_dl.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url[0], download=False)
            self.id = info_dict.get("id", None)
            ydl.download(url)
        os.chdir(root_dir)

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
        root_dir = config["youtube_converter"]["root_dir"]
        temp_dir = root_dir + "\\Temp"
        spotify_dir = config["youtube_converter"]["spotify_dir"]
        downloaded_file_path = temp_dir + "\\" + filename
        if filename[-4:] == "webm":
            processed_file_path = temp_dir + "\\" + filename[0:-5] + ".mp3"
        else:
            processed_file_path = temp_dir + "\\" + filename[0:-4] + ".mp3"
        result = subprocess.run(
            ["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-i", downloaded_file_path, "-acodec", "libmp3lame",
             "-ab",
             "128k", processed_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stderr:
            print(result.stderr)
        filename = os.path.splitext(filename)[0]
        final_file_path = spotify_dir + "\\" + filename + ".mp3"
        if self.artist is not None or self.title is not None:
            self.edit_tags(processed_file_path)
        try:
            os.rename(processed_file_path, final_file_path)
        except Exception as e:
            os.remove(downloaded_file_path)
            os.remove(processed_file_path)
            raise e
        try:
            os.remove(downloaded_file_path)
        except Exception as e:
            raise e


def main():
    Url(['https://www.youtube.com/watch?v=RPxvTd_jCPQ'], "Young Scrolls", "Sheogorath - Zoom")
    get_audio(["https://www.youtube.com/watch?v=xdOykEJSXIg"], "Anthony Hamilton", "Freedom")

if __name__ == "__main__":
    #print("nothing to do here")
    main()
