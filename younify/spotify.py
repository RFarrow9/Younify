import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import re
import json

with open('c:\\config\\config.json') as f:
    config = json.load(f)

def setup():
    client_credentials_manager = SpotifyClientCredentials(client_id=config["spotify"]["client_id"], client_secret=config["spotify"]["secret_id"])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

#first run the whole string against artist + song
#if success then use that metadata
#if fail, then run the searches seperately and stitch back together
#DO NOT order by popularity/pick by
#use the levenshtein distance against the potentials to rank

def request(name):
    name = name.lower()
    sp = setup()
    cleaned = clean(name)
    gen = consecutive_groups(cleaned)
    sp_artist = ""
    yt_artist = ""
    min = 100
    for i in gen:
        potential = " ".join(i)
        results = sp.search(q='artist:' + potential, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            for sub in name.split("-"):
                sp_artist = artist['name'].lower()
                sp_uri = artist['uri']
                yt_artist = sub.rstrip().lower()
                if min > levenshtein(sp_artist, yt_artist):
                    sp_artist_min = sp_artist
                    yt_artist_min = yt_artist
                    sp_uri_min = sp_uri
                    min = levenshtein(sp_artist, yt_artist)
    if min < 4:
        print("spotify artist: ", sp_artist_min)
        print("youtube artist: ", yt_artist_min)
        print("match confidence (0 is better): ", min)
    else:
        print("no confident match found")
    return sp_artist_min, sp_uri_min

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

def main():
    #artist, uri = request(r"Moderat -- Nr. 22 ( Official HD)")
    artist, song, success = artist_song_first_pass(r"A Quiet Place — How to Ruin Fear in 7 Seconds | Film Perfection")
    #albums = all_albums(uri)
    #songs = all_songs(uri)
    if success:
        print(artist)
        print(song)
    else:
        print("values not found")



    #print(results)

def artist_song_first_pass(string):
    cleanstring = clean(string)
    success = True
    if ' -- ' in cleanstring:
        artist, song = cleanstring.split(" -- ")
    elif ' - ' in cleanstring:
        artist, song = cleanstring.split(' - ')
    elif ' — ' in cleanstring:
        artist, song = cleanstring.split(' — ')
    elif 'by' in cleanstring:
        artist, song = cleanstring.split(' by ')
    else:
        artist, song, success = None, None, False
    return artist, song, success


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
    substitutions = {"original audio": ""
                     ,"( Official HD)": ""
                     ,"hq": ""
                     ,"official": ""
                     ,"video":""
                     ,"music":""
                     ,"lyrics":""}
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

def testing():
    search = cleantitle('James Bay \'Hear Your Heart\'')
    print(search)

    results = sp.search(q=search, limit=1)
    print(results)

def consecutive_groups(string="this is a test string"):
    input = tuple(string.split())
    for size in range(1, len(input)+1):
        for index in range(len(input)+1-size):
            yield input[index:index+size]

def first_pass(string):
    #do method
    #run against unfiltered information first
    sp = setup()
    #q = string.init(format:"artist:%@ track:%@", artistName, trackName)
    #sp.search(q, type="track", limit=5)
    results = sp.query

def second_pass():
    #do more expensive method
    print("tyest")


if __name__ == '__main__':
    main()
