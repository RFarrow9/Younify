from dataclasses import dataclass
import logzero
import typing
import configparser


"""""



"""""

#read the config file first and foremost
config = configparser.ConfigParser()
config.read("resources/config.ini")

# Do this better in future, needs an os agnostic method
log_location = "C:\\Users\\robfa\\PycharmProjects\\Younify\\younify_v2\\resources\\log.log"
if (logger := config['Logging']['log_location']) != "None":
    log_location = logger


def setup_logger(__name__: str, file_path: str = log_location, level: int = 10) -> logzero.logger:
    logzero.setup_default_logger()
    logzero.logfile(file_path, maxBytes=int(1e6))
    logzero.loglevel(level)
    return logzero.logger


spotify_dir = "C:\\Users\\robfa\\PycharmProjects\\Younify\\younify_v2\\temp"
youtube_options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'outtmpl': f"{spotify_dir}\%(title)s.%(ext)s",
            'quiet': True
        }


#set up spotify things
username = None
scope = None
client_id = None
client_secret = None
redirect_uri = None
cache_path = None


