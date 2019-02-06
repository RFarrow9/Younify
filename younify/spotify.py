import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import re

def setup():
    client_credentials_manager = SpotifyClientCredentials(client_id='', client_secret='')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#with open('config.json') as f:
    #config = json.load(f)

#playlists = sp.user_playlists('robbo1992')
#while playlists:
#    for i, playlist in enumerate(playlists['items']):
#        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#    if playlists['next']:
#        playlists = sp.next(playlists)
#   else:
#        playlists = None


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

#Could I use a basic neural network here?

    title = re.sub("(original audio)", "", title, flag)
    title = re.sub("\[original audio\]", "", title, flag)
    title = re.sub("(original video)", "", title, flag)
    title = re.sub("\[original video\]", "", title, flag)
    title = re.sub("(original music)", "", title, flag)
    title = re.sub("\[original music\]", "", title, flag)
    title = re.sub("(official music video)", "", title, flag)
    title = re.sub("\[official music video\]", "", title, flag)
    title = re.sub("(hq)", "", title, flag)
    title = re.sub("\[hq\]", "", title, flag)
    title = re.sub("(full)", "", title, flag)
    title = re.sub("\[full\]", "", title, flag)
    title = re.sub("(audio)", "", title, flag)
    title = re.sub("\[audio\]", "", title, flag)
    title = re.sub("(video)", "", title, flag)
    title = re.sub("\[video\]", "", title, flag)
    title = re.sub("(lyrics)", "", title, flag)
    title = re.sub("\[lyrics\]", "", title, flag)
    return title

def testing():
    search = cleantitle('James Bay \'Hear Your Heart\'')
    print(search)

    results = sp.search(q=search, limit=1)
    print(results)

