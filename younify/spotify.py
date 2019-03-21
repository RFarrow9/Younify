import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import re
import operator
import itertools
import json

"""
To use this...

"""

with open('c:\\config\\config.json') as f:
    config = json.load(f)

class SpotifyMatching:
    def __init__(self, name):
        self.name = name
        self.artist = None
        self.artist_uri = None
        self.song = None
        self.song_uri = None
        self.album = None
        self.album_uri = None
        self.sp = None
        self.success = True
        self.setup()

    def print(self):
        print("Name of video: " + str(self.name))
        print("Name of artist: " + str(self.artist))
        print("Artist URI: " + str(self.artist_uri))
        print("Name of Song: " + str(self.song))
        print("Song URI: " + str(self.song_uri))

    def setup(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=config["spotify"]["client_id"], client_secret=config["spotify"]["secret_id"])
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def artist_song_first_pass(self):
        if ' -- ' in self.name:
            self.artist, self.song = self.name.split(" -- ")
        elif ' - ' in self.name:
            self.artist, self.song = self.name.split(' - ')
        elif ' — ' in self.name:
            self.artist, self.song = self.name.split(' — ')
        elif ' by ' in self.name:
            self.artist, self.song = self.name.split(' by ')
        else:
            self.success = False
        if self.success:
            results = self.sp.search(q='artist: ' + self.artist + 'track: ' + self.song, type='track', limit=1)
            if results['tracks']['total'] >= 1:
                for items in results['tracks']['items']:
                    self.song = items['name']
                    self.song_uri = items['uri']
                    for artist in items['artists'][0]:
                        self.artist = artist['name']
                        self.artist_uri = artist['uri']
            else:
                self.success = False

    def artist_album_first_pass(self):
        """
        This method is untested, and very similar to the artist_song_first_pass method. There is probably a better way of doing this.
        """
        if ' -- ' in self.name:
            self.artist, self.album = self.album.split(" -- ")
        elif ' - ' in self.name:
            self.artist, self.album = self.name.split(' - ')
        elif ' — ' in self.name:
            self.artist, self.album = self.name.split(' — ')
        elif ' by ' in self.name:
            self.artist, self.album = self.name.split(' by ')
        else:
            self.success = False
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

    def artist_second_pass(self):
        gen = consecutive_groups(self.name)
        _min, cutoff = 100, 8
        sp_artist_min, sp_artist_uri_min = None, None
        for i in gen:
            potential = " ".join(i)
            results = self.sp.search(q='artist:' + potential, type='artist')
            items = results['artists']['items']
            if len(items) > 0:
                artist = items[0]
                if _min > cutoff:
                    for splitter in ["-", ",", " by "]:
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

    def artist_song_second_pass(self):
        if self.artist is not None:
            cleaned = self.name.lower().replace(self.artist, "")
            song_potentials = []
            gen = consecutive_groups(cleaned)
            for i in gen:
                potential = " ".join(i)
                results = self.sp.search(q="artist:" + self.artist + " track: " + potential, type="track", limit=1)
                if results['tracks']['total'] >= 1:
                    for items in results['tracks']['items']:
                        song_potentials.append([items['name'], items['uri']])
            self.song, self.song_uri = most_common(song_potentials)
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
            self.artist_song_second_pass()
        if self.success:
            #add to playlist here
            print("success")
        return self.success

    def return_song_artist(self):
        return self.song_uri, self.artist_uri

            #print("song not found in spotify")
            # push to playlists here?
            # push_to_playlist(playlistname)
            #print("should commence manual download here")

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1)
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1)
    return matrix[size_x - 1, size_y - 1]

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
    return regex.sub(lambda match: substitutions[match.group(0)], string)

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
    var =+ 1
    print(var)


if __name__ == '__main__':
    main()
