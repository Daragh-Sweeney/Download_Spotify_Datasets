import spotipy
import time
import random
from spotipy.oauth2 import SpotifyClientCredentials



import json

with open("spotify_credentials.json") as json_data_file:
    data = json.load(json_data_file)

client_id = data["client_id"]
client_secret = data["client_secret"]

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlists(
        category,
        country = "US"
):
    playlists = list()

    offset = 0
    while True: #get more playlists
        playlistResponse = sp.category_playlists(category, limit = 20, offset = offset, country = country)['playlists']
        playlists.extend(playlistResponse['items'])

        if playlistResponse['next'] == None:
            break
        else:
            offset += 20

    return playlists

def get_tracks(playlist):
    tracks = list()

    offset = 0
    while True: #get more playlists
        tracksResponse = sp.playlist_tracks(playlist['id'], limit=100, offset = offset)
        tracks.extend(tracksResponse['items'])

        if tracksResponse['next'] == None:
            break
        else:
            offset += 100

    return tracks

def get_album_images(category):
    print ("Downloading playlists")
    playlists = get_playlists(category)
    print ("Downloaded {} playlists".format(len(playlists)))

    print ("Downloading tracks")
    tracks = list()
    for playlist in playlists:
        tracks.extend(get_tracks(playlist))
    print ("Downloaded {} tracks".format(len(tracks)))

    allImages = set()
    for track in tracks:
        trackData = track['track']
        if (trackData == None): continue

        album = trackData['album']
        if (album == None): continue

        trackImages = album['images']
        if (trackImages == None or len(trackImages) == 0): continue

        imageUrl = trackImages[0]['url']

        if (imageUrl != None):
            allImages.add(imageUrl)

    return allImages


import urllib
import os


import http.client  # or http.client if you're on Python 3
http.client._MAXHEADERS = 1000

def download_url(url, root, filename=None):
    #root = os.path.expanduser(root)
    if not filename:
        filename = os.path.basename(url)
    fpath = os.path.join(root, filename  + "." + "png")

    os.makedirs(root, exist_ok=True)

    try:
        print('Downloading ' + url + ' to ' + fpath)
        urllib.request.urlretrieve(url, fpath)
    except (urllib.error.URLError, IOError) as e:
        if url[:5] == 'https':
            url = url.replace('https:', 'http:')
            print('Failed download. Trying https -> http instead.'
                  ' Downloading ' + url + ' to ' + fpath)
            urllib.request.urlretrieve(url, fpath)




categories = [
    "rock",
    "pop",
    "classical",
    "hiphop",
    "country",
    "latin",
    "edm_dance",
    "jazz"
]

#download all at once --> but it is ineffective if you have poor internet connection
"""for category in categories:
    print("-------------------------------")
    print("Downloading {}".format(category))
    print("-------------------------------")
    imageUrls = get_album_images(category)
    
    for url in imageUrls:
        download_url(url, "/content/gdrive/MyDrive/projects/images/" + category)"""


category = "edm_dance"
print("-------------------------------")
print("Downloading {}".format(category))
print("-------------------------------")
imageUrls = get_album_images(category)

for url in imageUrls:
    download_url(url, "projects/images/" + category)