import subprocess
import youtube_dl
import os
import eyed3
import json

with open('config.json') as f:
    config = json.load(f)


def get_audio(url, artist, title):
    root_dir = config["youtube_converter"]["root_dir"]
    temp_dir = root_dir + "\\Temp"
    spotify_dir = config["youtube_converter"]["spotify_dir"]
    options = {
        'format': 'bestaudio/best',  # choice of quality
        'extractaudio': True,  # only keep the audio
        'noplaylist': True,  # only download single song, not playlist
    }

    temp_contents = os.listdir(temp_dir)

    os.chdir(temp_dir)
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(url)
    os.chdir(root_dir)

    new_temp_contents = os.listdir(temp_dir)

    for x in temp_contents:
        if x in new_temp_contents:
            new_temp_contents.remove(x)

    for x in new_temp_contents:
        file_name, file_extension = os.path.splitext(x)
        downloaded_file_path = temp_dir + "\\" + x
        processed_file_path = temp_dir + "\\" + artist + "-" + title + ".mp3"
        subprocess.run(["cmd.bat", downloaded_file_path, processed_file_path])

        final_file_path = spotify_dir + "\\" + file_name + ".mp3"

        tag_file = eyed3.load(processed_file_path)
        tag_file.tag.artist = artist
        tag_file.tag.title = title
        tag_file.tag.album = title
        tag_file.tag.save()

        try:
            os.rename(processed_file_path, final_file_path)
        except Exception as e:
            raise e

        try:
            os.remove(downloaded_file_path)
        except Exception as e:
            raise e


def main():
    print("There's no main function.")
    get_audio(["https://www.youtube.com/watch?v=xdOykEJSXIg"], "Anthony Hamilton", "Freedom")


if __name__ == "__main__":
    main()
