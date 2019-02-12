import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import re
import sys

def setup():
    client_credentials_manager = SpotifyClientCredentials(client_id='', client_secret='')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp
#with open('config.json') as f:
    #config = json.load(f)

def request():
    sp = setup()
    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Radiohead'

    results = sp.search(q='artist:' + name, type='artist')
    print(results)
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        print(artist['name'], artist['images'][0]['url'])

def main():
    request()

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
    print (matrix)
    return (matrix[size_x - 1, size_y - 1])

def cleantitle(title):
    flag = re.IGNORECASE

    title = re.sub("[()]", "", title, flag).sub("[\[\]]", title, flag)
    title = re.sub("original audio", title, flag).sub("hq", title, flag)
    title = re.sub("official", title, flag).sub("video", title, flag)
    title = re.sub("music", title, flag).sub("lyrics", title, flag)
    return title

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
