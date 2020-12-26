#!/usr/bin/env python3
import os
import random
import spotipy
import time
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def getRandomSongs(audio_f):
    audio_features = []

    for i in range(50):
        offset = random.randint(0, 2000)
        query = getRandomSearch()
        songs = sp.search(query, limit=10, offset=offset)
        if(songs):
            for track in songs["tracks"]["items"]:
                id = track['id']
                features = sp.audio_features(id)
                removed = remove_features(audio_f, features[0])
                audio_features.append(removed)
    
    return audio_features

def getRandomSearch():
    characters = 'abcdefghijklmnopqrstuvwxyz'
    index = random.randint(0, 25)

    return characters[index] + '%'

def remove_features(features, item):
  ret = {}
  for f in features:
    ret[f] = item[f]
  return ret

def get_songs_from_user(audio_f, uid):
  playlists = sp.user_playlists('12176195123') #My user profile
  audio_features = []
  while playlists:
    print("Playlist names: ")  
    for i, playlist in enumerate(playlists['items']):
        tracks = sp.playlist_tracks(playlist['id'])
        print(playlist["name"])
        if tracks: 
          for j, track in enumerate(tracks['items']):
            id = track['track']['id']
            features = sp.audio_features(id)
            removed = remove_features(audio_f, features[0])
            audio_features.append(removed)
          
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
    print("Songs from user", uid, "have been added")
    return audio_features

 

def setup():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    cc_manager = SpotifyClientCredentials(client_id=client_id,
                                          client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=cc_manager)


# def add_album_songs(uri):
#     spotify_albums[uri] = {}
#     for attribute in song_attributes[:5]:
#         spotify_albums[uri][attribute] = []

#     tracks = sp.album_tracks(uri)
#     for item in tracks['items']:
#         spotify_albums[uri]['album'].append(album_names[album_count])
#         for attribute in song_attributes[1:5]:
#             spotify_albums[uri][attribute].append(item[attribute])


# def get_audio_features(album):
#     for attribute in song_attributes[5:]:
#         spotify_albums[album][attribute] = []

#     count = 0
#     for track in spotify_albums[album]['uri']:
#         features = sp.audio_features(track)
#         for attribute in song_attributes[5:-1]:
#             spotify_albums[album][attribute].append(features[0][attribute])

#         pop = sp.track(track)
#         spotify_albums[album]['popularity'].append(pop['popularity'])
#         count += 1


if __name__ == '__main__':
    sp = setup()
    result = sp.search('Wallows')

    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

    sp_albums = sp.artist_albums(artist_uri, album_type='album')

    song_attributes = ('album', 'track_number', 'id', 'name', 'uri', 'acousticness', 'danceability',
                       'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
                       'valence', 'popularity')
    
    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    # album_names = []
    # album_uris = []
    # for item in sp_albums['items']:
    #     album_names.append(item['name'])
    #     album_uris.append(item['uri'])

    # spotify_albums = {}

    # album_count = 0
    # for i in album_uris:
    #     add_album_songs(i)
    #     print('Songs from {} have been added to spotify_albums dictionary'.format(album_names[album_count]))
    #     album_count += 1

    # sleep_min = 2
    # sleep_max = 5
    # start_time = time.time()
    # request_count = 0
    # for i in spotify_albums:
    #     get_audio_features(i)
    #     request_count += 1
    #     if request_count % 5 == 0:
    #         print('{} playlists completed'.format(request_count))
    #         time.sleep(np.random.uniform(sleep_min, sleep_max))
    #         print('Loop #: {}'.format(request_count))
    #         print('Elapsed Time: {} seconds'.format(time.time() - start_time))

    # dict_df = {}
    # for attribute in song_attributes:
    #     dict_df[attribute] = []

    # for album in spotify_albums:
    #     for feature in spotify_albums[album]:
    #         dict_df[feature].extend(spotify_albums[album][feature])

    # df = pd.DataFrame.from_dict(dict_df)

    df_user = pd.DataFrame(get_songs_from_user(features, '12176195123'))
    n_user_songs = len(df_user.index)
    user_labels = np.ones(n_user_songs)

    df_random = pd.DataFrame(getRandomSongs(features))
    n_random_songs = len(df_random.index)
    random_labels = np.zeros(n_random_songs)
    labels = np.append(user_labels, random_labels)
    # print(labels)


    # print(df_random)
    # print(df_user)
    # print(getRandomSearch())

    data = pd.DataFrame.append(df_user, df_random)
    forest = RandomForestClassifier()
    forest_params = {
        "n_estimators": np.arange(10, 200, 10),
        "min_samples_leaf": np.arange(1, 100, 10),
        "max_features": ['auto', 'sqrt', 'log2']
    }
    clf = GridSearchCV(forest, forest_params)

    clf.fit(data, labels)
    print(clf.best_params_)


    # print('Original dataframe size: {}'.format(len(df)))
    # final_df = df.sort_values('popularity', ascending=False).drop_duplicates('name').sort_index()
    # print('Final dataframe size: {}'.format(len(final_df)))

    df_user.to_csv('./user_liked_songs.csv')
    df_random.to_csv('./random_songs.csv')
    # final_df.to_csv('./output.csv')



