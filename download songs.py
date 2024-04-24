import spotipy
import time
import random
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os
import urllib

with open("spotify_credentials.json") as json_data_file:
    data = json.load(json_data_file)

client_id = data["client_id"]
client_secret = data["client_secret"]

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlists(category, country="US"):
    playlists = list()
    offset = 0
    while True:
        playlistResponse = sp.category_playlists(category, limit=20, offset=offset, country=country)['playlists']
        playlists.extend(playlistResponse['items'])
        if playlistResponse['next'] is None:
            break
        else:
            offset += 20
    return playlists

def get_tracks(playlist):
    tracks = list()
    offset = 0
    while True:
        tracksResponse = sp.playlist_tracks(playlist['id'], limit=100, offset=offset)
        tracks.extend(tracksResponse['items'])
        if tracksResponse['next'] is None:
            break
        else:
            offset += 100
    return tracks

def download_track(track_url, root, filename):
    fpath = os.path.join(root, filename)
    os.makedirs(root, exist_ok=True)
    try:
        print('Downloading ' + track_url + ' to ' + fpath)
        urllib.request.urlretrieve(track_url, fpath)
    except (urllib.error.URLError, IOError) as e:
        print('Failed to download ' + track_url)

def download_tracks(tracks, root):
    for track in tracks:
        track_data = track['track']
        if track_data:
            track_name = track_data['name']
            artist_name = track_data['artists'][0]['name']
            track_url = track_data['preview_url']
            if track_url:
                filename = f"{artist_name} - {track_name}.mp3"
                download_track(track_url, root, filename)

def get_tracks_urls(playlist):
    tracks = get_tracks(playlist)
    track_urls = []
    for track in tracks:
        track_data = track['track']
        if track_data and track_data['preview_url']:
            track_urls.append(track_data['preview_url'])
    return track_urls

def download_random_tracks(playlists, root, num_tracks=1):
    for playlist in playlists:
        playlist_name = playlist['name']
        track_urls = get_tracks_urls(playlist)
        if track_urls:
            random_track_urls = random.sample(track_urls, min(num_tracks, len(track_urls)))
            for idx, track_url in enumerate(random_track_urls):
                download_track(track_url, root, f"{playlist_name}_{idx+1}.mp3")

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
category = "jazz"
num_tracks_per_playlist = 12  # Number of random tracks to download from each playlist
print("-------------------------------")
print(f"Downloading {num_tracks_per_playlist} random tracks from {category}")
print("-------------------------------")
playlists = get_playlists(category)
download_random_tracks(playlists, "projects/tracks/" + category, num_tracks_per_playlist)