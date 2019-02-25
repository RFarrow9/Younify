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
    success = True
    if ' -- ' in name:
        artist, song = name.split(" -- ")
    elif ' - ' in name:
        artist, song = name.split(' - ')
    elif ' — ' in name:
        artist, song = name.split(' — ')
    elif 'by' in name:
        artist, song = name.split(' by ')
    else:
        artist, song, success = None, None, False
    #return artist, song, success
    return success, artist, song

def artist_second_pass(name):
    name = name.lower()
    sp = setup()
    cleaned = clean(name)
    gen = consecutive_groups(cleaned)
    _min, cutoff = 100, 8
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
                            sp_uri_min = sp_uri
                            _min = levenshtein(sp_artist, yt_artist)
    if min >= cutoff:
        print("no confident match found")
    return sp_artist_min, sp_uri_min

def song_second_pass(name="Sufjan Stevens, Fourth Of July (Official Audio)"):
    sp_artist, sp_uri = artist_second_pass(name)
    sp = setup()
    artist_removed = name.lower().replace(sp_artist, "")
    cleaned = clean(artist_removed)
    song_potentials = []
    gen = consecutive_groups(cleaned)
    min = 100
    cutoff = 8
    for i in gen:
        potential = " ".join(i)
        results = sp.search(q="artist:" + sp_artist + " track: " + potential, type="track", limit=1)
        if results['tracks']['total'] >= 1:
            for items in results['tracks']['items']:
                song_potentials.append(items['name'])
    #print(most_common(song_potentials))
    #if min > cutoff:
    #    print("no confident match found")
    #    sp_song = None
    #else:
    sp_song = most_common(song_potentials)
    return sp_song

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
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 1, size_y - 1])

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
    min_index = len(L)
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


    artist, song, success = artist_song_first_pass(name)
    song_found = False
    if success:
        q = "artist:" + artist + " track:" + song
        results = sp.search(q, type="track", limit=1)
        if results['tracks']['total'] >= 1:
            for items in results['tracks']['items']:
                song_id = items['uri']
            song_found = True
        else:
            song_found = False
    #else:
    #    print("First pass failure, moving onto second pass")
    if not success:
        artist, uri = artist_second_pass(name)
        song = song_second_pass(name)
        print("artist: " + artist)
        print("song: " + song)

if __name__ == '__main__':
    main()