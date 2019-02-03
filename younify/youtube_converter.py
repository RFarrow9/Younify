import subprocess
import youtube_dl
import os
import eyed3

root_dir = "C:\\Users\\robfa\\Documents\\Python\\Youtube Thing"
temp_dir = root_dir + "\\Temp"
spotify_dir = "C:\\Users\\robfa\\Music\\From YouTube"

def get_audio(url, artist, title):
    options = {
        'format': 'bestaudio/best',         # choice of quality
        'extractaudio': True,               # only keep the audio
        'noplaylist': True,                 # only download single song, not playlist
        'progress_hooks': [my_hook],
        'outtmpl': '%(title)s.%(ext)s'
    }
    os.chdir(temp_dir)
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(url)
    os.chdir(root_dir)

def my_hook(d):
    if d['status'] == 'finished':
        convert(d['filename'])
        #print("Done downloading {}".format(file_tuple[1]))
    #if d['status'] == 'downloading':
        #print(d['filename'], d['_percent_str'], d['_eta_str'])

def convert(filename):
    downloaded_file_path = temp_dir + "\\" + filename
    if filename[-4:] == "webm":
        processed_file_path = temp_dir + "\\" + filename[0:-5] + ".mp3"
    else:
        processed_file_path = temp_dir + "\\" + filename[0:-4] + ".mp3"
    result = subprocess.run(
        ["C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-i", downloaded_file_path, "-acodec", "libmp3lame", "-ab",
         "128k", processed_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        print(result.stderr)
    final_file_path = spotify_dir + "\\" + filename[0:-5] + ".mp3"
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

    get_audio(['https://www.youtube.com/watch?v=RPxvTd_jCPQ'], "Young Scrolls", "Sheogorath - Zoom")


if __name__ == "__main__":
    print("nothing to do here")
    #main()

