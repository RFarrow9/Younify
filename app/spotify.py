import spotipy
from . import *
import spotipy.util

from singleton_decorator import singleton

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
class Spotify:
    sp: object = None

    def __post_init__(self):
        self.create_token()

    def create_token(self):
        token = None

        def token_helper():
            return spotipy.util.prompt_for_user_token(
                username=username,
                scope=scope,
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri
            )

        token = token_helper()
        if token:
            log.info(f"Spotify token successfully generated for user: {username}.")
        else:
            log.error(f"Failure during spotify token generation for user: {username}.")

    def all_songs(self, artist):
        log.debug("Called all_songs for %s." % artist)
        songs = []
        albums = self.all_albums(artist)
        for album in albums:
            results = self.album_tracks(album['uri'])
            for item in results:
                songs.extend(item['name'])
        for song in songs:
            print(song)
        return songs

    def all_albums(self, artist):
        log.debug("Called all_albums for %s." % artist)
        results = self.sp.artist_albums(self.artist_uri, album_type='album')
        albums = results['items']
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return albums

    def album_tracks(self, album_uri):
        pass

    def artist_albums(self, artist_uri):
        pass

    def artist_uri(self, artist_string):
        """
        1. Check if in cache first
        2. If in cache but old, or not in cache
        3. Run the artist string against spotify api
        4. Parse results, check if valid artist

        TODO: Be aware of API call overloading, we would be better of sending these in batches (use async?)
        """
        pass