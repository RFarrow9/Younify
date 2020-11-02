import spotipy
from . import *
import spotipy.util
import os

from singleton_decorator import singleton
from spotipy import oauth2

"""""

Holds the spotify singleton. This class is used as the communicator with spotify.


To find a song, we:
    1a. If there is an artist given, jump to 2.
    1b. Identify the most likely artist
    2a. Check if the artist already exists in the cache, if it is, get this information. 
    2b. For the artist, get the artist uri
    3. For the artist, identify all the albums
    4. For each of the albums, get all the songs
    5. Put these into a cache for future use (cache expires with the program)
    6. Compare the remaining part of the string with the songs in the cache via levenshtein
    
For a playlist:
    1. Identify if single artist or multiple (if single - is it an album)
    2. Identify the timestamps of the songs
    3. Identify any strings associated with the timestamps 
    4. Instantiate a song object for each of the 'strings' with artist already given
    
"""""

log = setup_logger(__name__)


@singleton
@dataclass
class SpotifySingleton:
    sp: object = None

    def set_sp(self):
        """Gets the spotipy handler"""
        credentials = oauth2.SpotifyClientCredentials(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"))
        token = credentials.get_access_token()
        self.sp = spotipy.Spotify(auth=token)

    def artist_albums(self, artist_id):
        return self.sp.artist_albums(artist_id)

    def artist_uri(self, artist_string):
        """
        1. Check if in cache first
        2. If in cache but old, or not in cache
        3. Run the artist string against spotify api
        4. Parse results, check if valid artist

        TODO: Be aware of API call overloading, we would be better of sending these in batches (use async?)
        """
        pass