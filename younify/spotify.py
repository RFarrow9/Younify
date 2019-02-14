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
                if min > levenshtein(artist['name'], sub):
                    sp_artist = artist['name']
                    yt_artist = sub
                    min = levenshtein(artist['name'], sub)
    if min < 4:
        print("spotify artist: ", sp_artist)
        print("youtube artist: ", yt_artist)
        print("match confidence (0 is better): ", min)
    else:
        print("no confident match found")

def main():
    request(r"Moderat -- Nr. 22 ( Official HD)")

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

def cleantitle(title):
    flag = re.IGNORECASE
    title = re.sub("[()]", "", title, flag)
    title = re.sub(r"[\[\]]", title, flag)
    title = re.sub("original audio", title, flag)
    title = re.sub("hq", title, flag)
    title = re.sub("official", title, flag)
    title = re.sub("video", title, flag)
    title = re.sub("music", title, flag)
    title = re.sub("lyrics", title, flag)
    title = re.sub("[-]", title, flag)
#Could I use a basic neural network here?

    title = re.sub("[()]", "", title, flag).sub("[\[\]]", title, flag)
    title = re.sub("original audio", title, flag).sub("hq", title, flag)
    title = re.sub("official", title, flag).sub("video", title, flag)
    title = re.sub("music", title, flag).sub("lyrics", title, flag)
    return title.lower()


def clean(string):
    substitutions = {"original audio": ""
                     ,"- ": ""
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


if __name__ == '__main__':
    main()
