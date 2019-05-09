import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import numpy as np
import re
import operator
import itertools
import sys
import json

"""
This is the module that handles interfacing with spotify. It is pulled in from the YoutubeSongs/Playlist classes in the youtube converter module.
This will then check the information against spotify to match if possible with a spotify song (or album?).

This needs to have some sort of authentication to work fully. For this it may need extension to have a wrapper class that holds persistent state.
Investigate this authentication further, can we use any of the results to authenticate user in younify?
"""

with open('c:\\config\\config.json') as f:
    config = json.load(f)

splitters = ["--", " - ", " — ", " by ", "//"]


class SpotifyMatching:
    def __init__(self, name):
        self.name = name
        self.name_clean = clean(name)
        self.artist = None
        self.artist_uri = None
        self.song = None
        self.song_uri = None
        self.album = None
        self.album_uri = None
        self.sp = None
        self.success = True
        self.playlist_uri = None
        self.setup()

    def print(self):
        print("Name of video: " + str(self.name))
        print("Name of artist: " + str(self.artist))
        print("Artist URI: " + str(self.artist_uri))
        print("Name of Song: " + str(self.song))
        print("Song URI: " + str(self.song_uri))

    def setup(self):
        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            print("Usage: %s username" % (sys.argv[0],))
            sys.exit()
        token = util.prompt_for_user_token(username)
        if token:
            self.sp = spotipy.Spotify(auth=token)
        else:
            print("Couldn't obtain token for user")
        #client_credentials_manager = SpotifyClientCredentials(client_id=config["spotify"]["client_id"], client_secret=config["spotify"]["secret_id"])
        #self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def artist_song_first_pass(self):
        self.success = False
        song_potentials = []
        index = 0
        _min = 20
        def inner(index):
            results = self.sp.search(q='artist: ' + self.artist + 'track: ' + self.song, type='track', limit=5)
            if results['tracks']['total'] >= 1:
                for items in results['tracks']['items']:
                    song_potentials.append([items['name'], items['uri']])
                    for artist in items['artists']:
                        song_potentials[index].append([artist['name'], artist['uri']])
                    index += 1
        for splitter in splitters:
            if splitter in self.name_clean:
                self.artist, self.song = self.name_clean.split(splitter)
                inner(index)
        cutoff = matching(self.name_clean)
        for potentials in song_potentials:
            if levenshtein(self.name_clean, potentials[0] + potentials[2]) < min:
                _min = levenshtein(self.name_clean, potentials[0] + potentials[2])
                self.artist = potentials[2]
                self.artist_uri = potentials[3]
                self.song = potentials[0]
                self.song_uri = potentials[1]
        if self.artist and self.song is not None:
            if levenshtein(self.name_clean, self.artist + self.song) > cutoff:
                self.success = False
                self.artist = None
                self.song = None
            else:
                self.success = True
        else:
            self.success = False


    def artist_album_first_pass(self):
        """
        This method is untested, and very similar to the artist_song_first_pass method. There is probably a better way of doing this.
        """
        self.success = False
        for splitter in splitters:
            if splitter in self.name:
                self.artist, self.album = self.name.split(splitter)
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

    def artist_second_pass_old(self):
        gen = consecutive_groups(self.name)
        _min = 100
        cutoff = matching(self.name)
        sp_artist_min, sp_artist_uri_min = None, None
        for i in gen:
            potential = " ".join(i)
            results = self.sp.search(q='artist:' + potential, type='artist')
            items = results['artists']['items']
            if len(items) > 0:
                artist = items[0]
                if _min > cutoff:
                    for splitter in ["-", ",", " by ", "//"]:
                        for sub in self.name.split(splitter):
                            sp_artist = artist['name'].lower()
                            sp_uri = artist['uri']
                            yt_artist = sub.rstrip().lower()
                            if _min > levenshtein(sp_artist, yt_artist):
                                sp_artist_min = sp_artist
                                sp_artist_uri_min = sp_uri
                                _min = levenshtein(sp_artist, yt_artist)
        if _min >= cutoff:
            self.success = False
        else:
            self.artist = sp_artist_min
            self.artist_uri = sp_artist_uri_min

    def artist_second_pass(self):
        gen = consecutive_groups(self.name_clean)
        _min = 100
        cutoff = matching(self.name_clean)
        sp_artist_min, sp_artist_uri_min = None, None
        for splitter in ["-", ",", " by ", "//"]:
            if splitter in self.name_clean:
                for sub in self.name_clean.split(splitter):
                    yt_artist = sub.rstrip().lower()
                    for i in gen:
                        potential = " ".join(i)
                        results = self.sp.search(q='artist:' + potential, type='artist')
                        items = results['artists']['items']
                        if len(items) > 0:
                            artist = items[0]
                            sp_artist = artist['name'].lower()
                            sp_uri = artist['uri']
                            if _min > levenshtein(sp_artist, yt_artist):
                                sp_artist_min = sp_artist
                                sp_artist_uri_min = sp_uri
                                _min = levenshtein(sp_artist, yt_artist)
        if _min >= cutoff:
            self.success = False
        else:
            self.artist = sp_artist_min
            self.artist_uri = sp_artist_uri_min

    def song_second_pass(self):
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
            cutoff = matching(self.name_clean)
            if levenshtein(self.name_clean, self.artist + self.song) > cutoff:
                self.success = False
            else:
                self.success = True
            # handle cases where every 'song' appears just once - levenshtein back to original string (minus the artist)

    def all_songs(self):
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
        results = self.sp.artist_albums(self.artist_uri, album_type='album')
        albums = results['items']
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return albums

    def process(self):
        self.artist_song_first_pass()
        if not self.success:
            print("first pass failure, proceeding to second..")
            self.artist_second_pass()
            self.song_second_pass()
        if self.success:
            self.add_to_playlist()
        else:
            print("second pass failure.. song not found")
        print("artist: " + self.artist)
        print("song: " + self.song)
        return self.success

    def add_to_playlist(self, playlist_uri="None"):
        """"Not sure how this should work, currently the playlist is a class attribute
        , if it should be a class attribute, should it be an array?"""
        if self.playlist_uri == "None":
            return
        else:
            results = self.sp.user_playlist_add_tracks(self.playlist_uri, self.song_uri)
            print(results)

    def return_song_artist(self):
        return self.song_uri, self.artist_uri

            #print("song not found in spotify")
            # push to playlists here?
            # push_to_playlist(playlistname)
            #print("should commence manual download here")


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1)
            else:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1)
    return matrix[size_x - 1, size_y - 1]


def matching(string):
    if len(string) <= 4:
        return 0
    elif len(string) <= 6:
        return 1
    elif len(string) <= 9:
        return 2
    else:
        return 3

def clean(string):
    string = string.lower()
    substitutions = {"original audio":""
                     ,"hq": ""
                     ,"official": ""
                     ,"video":""
                     ,"music":""
                     , ", ":" "
                     , ",": " "
                     ,"lyrics":""}
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    string = re.sub("[\(\[].*?[\)\]]", "", string)
    return str(regex.sub(lambda match: substitutions[match.group(0)], string))

def consecutive_groups(string="this is a test string"):
    input = tuple(string.split())
    for size in range(1, len(input)+1):
        for index in range(len(input)+1-size):
            yield input[index:index+size]

def most_common(_list):
  SL = sorted((x, i) for i, x in enumerate(_list))
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(_list)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    return count, -min_index
  return max(groups, key=_auxfun)[0]


def main():
    print("Nothing to do here.")


if __name__ == '__main__':
    main()
