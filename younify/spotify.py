import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import re
import operator
import itertools
import json

with open('c:\\config\\config.json') as f:
    config = json.load(f)

def setup():
    client_credentials_manager = SpotifyClientCredentials(client_id=config["spotify"]["client_id"], client_secret=config["spotify"]["secret_id"])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def artist_song_first_pass(name):
    artist, artist_uri, song, song_uri, success = None, None, None, None, True
    if ' -- ' in name:
        artist, song = name.split(" -- ")
    elif ' - ' in name:
        artist, song = name.split(' - ')
    elif ' — ' in name:
        artist, song = name.split(' — ')
    elif 'by' in name:
        artist, song = name.split(' by ')
    else:
        artist, artist_uri, song, song_uri, success = None ,None, None, None, False
    if success:
        sp = setup()
        results = sp.search(q='artist: ' + artist + 'track: ' + song, type='track', limit=1)
        if results['tracks']['total'] >= 1:
            for items in results['tracks']['items']:
                song = items['name']
                song_uri = items['uri']
                for artist in items['artists'][0]:
                    artist = artist['name']
                    artist_uri = artist['uri']
        else:
            success = False
    return  artist, artist_uri, song, song_uri, success

def artist_second_pass(name):
    name = name.lower()
    sp = setup()
    cleaned = clean(name)
    gen = consecutive_groups(cleaned)
    _min, cutoff, success = 100, 8, True
    sp_artist_min, sp_artist_uri_min = None, None
    for i in gen:
        potential = " ".join(i)
        results = sp.search(q='artist:' + potential, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            if _min > cutoff:
                for splitter in ["-", ",", " by "]:
                    for sub in name.split(splitter):
                        sp_artist = artist['name'].lower()
                        sp_uri = artist['uri']
                        yt_artist = sub.rstrip().lower()
                        if _min > levenshtein(sp_artist, yt_artist):
                            sp_artist_min = sp_artist
                            sp_artist_uri_min = sp_uri
                            _min = levenshtein(sp_artist, yt_artist)
    if _min >= cutoff:
        success = False
    return sp_artist_min, sp_artist_uri_min, success

def artist_song_second_pass(name):
    sp_artist, sp_artist_uri, success = artist_second_pass(name)
    sp_song, sp_song_uri = None, None
    if success:
        sp = setup()
        cleaned = name.lower().replace(sp_artist, "")
        song_potentials = []
        gen = consecutive_groups(cleaned)
        for i in gen:
            potential = " ".join(i)
            results = sp.search(q="artist:" + sp_artist + " track: " + potential, type="track", limit=1)
            if results['tracks']['total'] >= 1:
                for items in results['tracks']['items']:
                    song_potentials.append([items['name'], items['uri']])
        sp_song, sp_song_uri = most_common(song_potentials)
        success = True
        #handle cases where every 'song' appears just once - levenshtein back to original string (minus the artist)
    return sp_artist, sp_artist_uri, sp_song, sp_song_uri, success

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
    substitutions = {"original audio":""
                     ,"hq": ""
                     ,"official": ""
                     ,"video":""
                     ,"music":""
                     , ", ":" "
                     , ",": " "
                     , "(official audio)": ""
                     , "( Official hd)": ""
                     , "(Official video)": ""
                     ,"lyrics":""}
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    #bit of code that removes everything in brackets?
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

def all_songs(artist_uri):
    sp = setup()
    songs = []
    albums = all_albums(artist_uri)
    for album in albums:
        results = sp.album_tracks(album['uri'])
        for item in results:
            songs.extend(item['name'])
    for song in songs:
        print(song)
    return songs

def all_albums(uri):
     sp = setup()
     results = sp.artist_albums(uri, album_type='album')
     albums = results['items']
     while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
     return albums

def process(name):
    sp = setup()
    name = clean(name)
    artist, artist_uri, song, song_uri, success = artist_song_first_pass(name)
    if not success:
        artist, artist_uri, song, song_uri, success = artist_song_second_pass(name)
    if not success:
        print("song not found in spotify")
        #push to playlists here?
        #push_to_playlist(playlistname)
        print("should commence manual download here")
    return success

if __name__ == '__main__':
    main()