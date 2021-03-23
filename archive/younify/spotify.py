from younify import *
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy
import numpy as np
import itertools
import operator
from dataclasses import dataclass
import tenacity

"""
This is the module that handles interfacing with spotify. It is pulled in from the YoutubeSongs/Playlist classes in the youtube converter module.
This will then check the information against spotify to match if possible with a spotify song (or album?).

We should not instantiate this per video, but rather we should use a single instance, and pass it the queries.
"""


def create_token():
    """
        This function generates a global token for authentication. It has been removed from the class itself to
        avoid calling this function multiple times as it only needs to be used as a singleton.

        It will make a second attempt if the first one fails, this can take up to 200 seconds whilst waiting for
        internet connection if this is severed.
    """
    def token_helper():
        token = util.prompt_for_user_token(username="robbo1992", scope='user-library-read playlist-modify-private playlist-modify',
                                           client_id=config["spotify"]["client_id"], client_secret=config["spotify"]["secret_id"],
                                           redirect_uri='http://localhost:8080', cache_path=spotify_cache)
        return token
    if token_helper():
        log.debug("Succesfully generated a spotify token for authentication")
        return spotipy.Spotify(auth=token_helper())
    else:
        if motley.internet:
            if token_helper():
                log.debug("Succesfully generated a spotify token for authentication")
                return spotipy.Spotify(auth=token_helper())
            else:
                log.error("Authentication error in create_token method.")


splitters = ["--", " - ", " — ", " by ", "//"]
log = motley.setup_logger(__name__)
token = create_token()

class SpotifyMatching:
    def __init__(self, name, token=token):
        self.name = name
        self.name_clean = clean(name)
        self.artist = None
        self.artist_uri = None
        self.song = None
        self.song_uri = None
        self.album = None
        self.album_uri = None
        self.sp = token
        self.success = True
        self.playlist_uri = None

    def print(self):
        print("Name of video: " + str(self.name))
        print("Name of artist: " + str(self.artist))
        print("Artist URI: " + str(self.artist_uri))
        print("Name of Song: " + str(self.song))
        print("Song URI: " + str(self.song_uri))

    def log_attributes(self):
        log.info("--Attributes for %s" % id(self))
        log.info("Name of video: %s" % str(self.name))
        log.info("Name of artist: %s" % str(self.artist))
        log.info("Artist URI: %s" % str(self.artist_uri))
        log.info("Name of Song: %s" % str(self.song))
        log.info("Song URI: %s" % str(self.song))

    def artist_song_first_pass(self):
        """
            This is the first attempt at generating the artist + song from the youtube title string.
            This works by splitting the string based on a global set of potential artist/song splits,
            and running all sequential sets against the spotipy api.
            This is typically lightweight, and should only result in a couple API calls.
        """
        log.debug("Called artist_song_first_pass for %s." % self.name)
        self.success = False
        song_potentials = []
        potential_count = 0
        _min = 20

        def generate_potentials(count):
            results = self.sp.search(q= 'artist: ' + self.artist + ' track: ' + self.song, type='track', limit=2)
            if results['tracks']['total'] >= 1:
                for items in results['tracks']['items']:
                    song_potentials.append([items['name'], items['uri']])
                    for artist in items['artists']:
                        song_potentials[count].append(artist['name'])
                        song_potentials[count].append(artist['uri'])
                    count += 1

        for splitter in splitters:
            if self.name_clean.count(splitter) == 1:
                self.artist, self.song = self.name_clean.split(splitter)
                generate_potentials(potential_count)
            elif self.name_clean.count(splitter) > 1:
                for x in range(0, self.name_clean.count(splitter)):
                    self.artist, self.song = split(self.name_clean, splitter, x)
                    generate_potentials(potential_count)

        cutoff = matching(self.name_clean)
        log.debug("%s potential matches found for %d" % (len(song_potentials), id(self)))
        log.debug("Potentials: %s" % song_potentials)
        for potential in song_potentials:
            log.debug(potential)
            log.debug(self.name_clean)
            log.debug(str(potential[2]) + " " + str(potential[0]))
            lev = levenshtein(self.name_clean, str.lower(str(potential[2])) + " " + str.lower(str(potential[0])))
            log.debug(lev)
            if lev < _min:
                _min = lev
                self.artist = potential[2]
                self.artist_uri = potential[3]
                self.song = potential[0]
                self.song_uri = potential[1]

        if self.artist_uri and self.song_uri is not None:
            log.debug("Cutoff point for %s : %d" % (id(self), cutoff))
            log.debug("Current Min: {}".format(_min))
            log.debug("Levenshtein distance between {} and {} :  {}"
                      .format(self.name_clean, self.artist + self.song,
                              levenshtein(self.name, self.artist + " " + self.song)))
            if int(_min) > cutoff:
                log.debug("Method artist_song_first_pass failed for %s." % self.name)
                self.success = False
                self.artist = None
                self.song = None
            else:
                log.debug("Method artist_song_first_pass succeeded for %s." % self.name)
                self.success = True
        else:
            log.debug("Method artist_song_first_pass failed for %s." % self.name)
            self.success = False
            self.artist = None
            self.song = None

    def artist_second_pass(self):
        """
            This is the first attempt at generating the artist + song from the youtube title string.
            This works by splitting the string based on a global set of potential artist/song splits,
            and running all sequential sets against the spotipy api.
            This is typically lightweight, and should only result in a couple API calls.
        """
        log.debug("Called artist_second_pass for %s." % self.name)
        gen = consecutive_groups(self.name_clean)
        _min = 100
        cutoff = matching(self.name_clean)
        sp_artist_min, sp_artist_uri_min = None, None
        self.success = False

        for splitter in splitters:
            if splitter in self.name_clean:
                for sub in self.name_clean.split(splitter):
                    yt_artist = sub.rstrip().lower()
                    for i in gen:
                        potential = " ".join(i)
                        results = self.sp.search(q='artist:' + potential, type='artist', limit=2)
                        items = results['artists']['items']
                        if len(items) > 0:
                            artist = items[0]
                            sp_artist = artist['name'].lower()
                            sp_uri = artist['uri']
                            lev = levenshtein(sp_artist, yt_artist)
                            if _min > lev:
                                sp_artist_min = sp_artist
                                sp_artist_uri_min = sp_uri
                                _min = lev

        if _min <= cutoff:
            log.debug("Method artist_second_pass succeeded for %s." % self.name)
            self.artist = sp_artist_min
            self.artist_uri = sp_artist_uri_min
            self.success = True
        else:
            log.debug("Method artist_second_pass failed for %s." % self.name)
            self.success = False

    def song_second_pass(self):
        """

        """
        log.debug("Called song_second_pass for %s." % self.name)
        if self.artist is not None:
            cleaned = self.name_clean.lower().replace(self.artist, "")
            song_potentials = []
            gen = consecutive_groups(cleaned)

            for i in gen:
                potential = " ".join(i)
                results = self.sp.search(q="artist:" + self.artist + " track: " + potential, type="track", limit=1)
                if results['tracks']['total'] >= 1:
                    for items in results['tracks']['items']:
                        song_potentials.append([items['name'], items['uri']])
            if len(song_potentials) >= 2:
                self.song, self.song_uri = most_common(song_potentials)
            elif len(song_potentials) == 1:
                self.song = song_potentials[0][0]
                self.song_uri = song_potentials[0][1]
            else:
                self.success = False
            if self.success:
                cutoff = matching(self.name_clean)
                if levenshtein(self.name_clean, self.artist + self.song) > cutoff:
                    log.debug("Method song_second_pass failed for %s." % self.name)
                    self.success = False
                else:
                    log.debug("Method song_second_pass succeeded for %s." % self.name)
                    self.success = True
                # handle cases where every 'song' appears just once - levenshtein back to original string (minus the artist)
            log.debug("The method song_second_pass was called without a valid artist.")
            self.success = False

    def album_assignment(self):
        """
        This method is untested, and very similar to the artist_song_first_pass method. There is probably a better way of doing this.
        """
        log.debug("Called album_assignment for %s." % self.name)
        self.success = False
        for splitter in splitters:
            if splitter in self.name:
                self.artist, self.album = self.name.split(splitter, 1)  # May need to look at this again, can be more than 1!
                self.success = True
                break
        if self.success:
            results = self.sp.search(q='artist: ' + self.artist + 'album: ' + self.album, type='album', limit=1)
            if results['albums']['total'] >= 1:
                for items in results['albums']['items']:
                    self.album = items['name']
                    self.album_uri = items['uri']
                    for artist in items['artists'][0]:
                        self.artist = artist['name']
                        self.artist_uri = artist['uri']
            else:
                self.success = False

    def all_songs(self):
        log.debug("Called all_songs for %s." % self.name)
        songs = []
        albums = self.all_albums()
        for album in albums:
            results = self.sp.album_tracks(album['uri'])
            for item in results:
                songs.extend(item['name'])
        for song in songs:
            print(song)
        return songs

    def all_albums(self):
        log.debug("Called all_albums for %s." % self.name)
        results = self.sp.artist_albums(self.artist_uri, album_type='album')
        albums = results['items']
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return albums

    def process(self):
        log.debug("Called process for %s." % self.name)
        self.artist_song_first_pass()
        self.log_attributes()
        if not self.success:
            self.artist_second_pass()
            self.song_second_pass()
        if self.success:
            self.add_to_playlist()
        return self.success

    def add_to_playlist(self, playlist_uri="spotify:playlist:3VUBchphbcLwE5WdqBW3gv", user="robbo1992"):
        """"
        Not sure how this should work, currently the playlist is a class attribute, if it should be
        a class attribute, should it be a list?
        """
        if playlist_uri is None or self.song_uri is None:
            log.warn("Object attributes are None, cannot add to playlist.")
            return
        else:
            log.debug("Adding song %s to playlist." %str(self.song_uri))
            results = self.sp.user_playlist_add_tracks(user, playlist_uri, [self.song_uri])
            log.debug("Adding to playlist results: %s" % results)

    def return_song_artist(self):
        return self.song_uri, self.artist_uri





@dataclass
class Matcher:
    token: spotipy.Spotify = None

    def __post_init__(self):
        self.token = self.get_token()

    @staticmethod
    def get_token():
        """This function will create the spotify token"""

        def token_helper():
            token = util.prompt_for_user_token(username="robbo1992",
                                               scope='user-library-read playlist-modify-private playlist-modify',
                                               client_id=config["spotify"]["client_id"],
                                               client_secret=config["spotify"]["secret_id"],
                                               redirect_uri='http://localhost:8080', cache_path=spotify_cache)
            return token

        if token_helper():
            log.debug("Succesfully generated a spotify token for authentication")
            return spotipy.Spotify(auth=token_helper())
        else:
            if motley.internet:
                if token_helper():
                    log.debug("Succesfully generated a spotify token for authentication")
                    return spotipy.Spotify(auth=token_helper())
                else:
                    log.error("Authentication error in create_token method.")
                    raise Exception
