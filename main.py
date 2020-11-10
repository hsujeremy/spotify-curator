#!/usr/bin/env python3
import os
import spotipy
import time
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


def setup():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    cc_manager = SpotifyClientCredentials(client_id=client_id,
                                          client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=cc_manager)


def add_album_songs(uri):
    spotify_albums[uri] = {}
    for attribute in song_attributes[:5]:
        spotify_albums[uri][attribute] = []

    tracks = sp.album_tracks(uri)
    for item in tracks['items']:
        spotify_albums[uri]['album'].append(album_names[album_count])
        for attribute in song_attributes[1:5]:
            spotify_albums[uri][attribute].append(item[attribute])


def get_audio_features(album):
    for attribute in song_attributes[5:]:
        spotify_albums[album][attribute] = []

    count = 0
    for track in spotify_albums[album]['uri']:
        features = sp.audio_features(track)
        for attribute in song_attributes[5:-1]:
            spotify_albums[album][attribute].append(features[0][attribute])

        pop = sp.track(track)
        spotify_albums[album]['popularity'].append(pop['popularity'])
        count += 1


if __name__ == '__main__':
    sp = setup()
    result = sp.search('Wallows')

    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

    sp_albums = sp.artist_albums(artist_uri, album_type='album')

    song_attributes = ('album', 'track_number', 'id', 'name', 'uri', 'acousticness', 'danceability',
                       'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
                       'valence', 'popularity')

    album_names = []
    album_uris = []
    for item in sp_albums['items']:
        album_names.append(item['name'])
        album_uris.append(item['uri'])

    spotify_albums = {}

    album_count = 0
    for i in album_uris:
        add_album_songs(i)
        print('Songs from {} have been added to spotify_albums dictionary'.format(album_names[album_count]))
        album_count += 1

    sleep_min = 2
    sleep_max = 5
    start_time = time.time()
    request_count = 0
    for i in spotify_albums:
        get_audio_features(i)
        request_count += 1
        if request_count % 5 == 0:
            print('{} playlists completed'.format(request_count))
            time.sleep(np.random.uniform(sleep_min, sleep_max))
            print('Loop #: {}'.format(request_count))
            print('Elapsed Time: {} seconds'.format(time.time() - start_time))

    dict_df = {}
    for attribute in song_attributes:
        dict_df[attribute] = []

    for album in spotify_albums:
        for feature in spotify_albums[album]:
            dict_df[feature].extend(spotify_albums[album][feature])

    df = pd.DataFrame.from_dict(dict_df)

    print('Original dataframe size: {}'.format(len(df)))
    final_df = df.sort_values('popularity', ascending=False).drop_duplicates('name').sort_index()
    print('Final dataframe size: {}'.format(len(final_df)))

    final_df.to_csv('./output.csv')



