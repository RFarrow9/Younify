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
log_location = "C:\\Users\\robf\\Documents\\Git\\Younify\\younify_v2\\resources\\log.log"
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
username = "robbo1992"
scope = "user-library-read playlist-modify-private playlist-modify"
client_id = config["spotify"]["client_id"]
client_secret = config["spotify"]["secret_id"]
redirect_uri = "http://localhost:8080"
cache_path = None


