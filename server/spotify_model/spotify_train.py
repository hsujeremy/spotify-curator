#!/usr/bin/env python3
import os
import random
import spotipy
import time
import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV


def getRandomSongs(audio_f):
    audio_features = []

    for i in range(200):
        offset = random.randint(0, 500)
        print(offset)

        query = getRandomSearch()
        print(query)
        songs = sp.search(query, limit=10, offset=offset)
        if(songs):
            for track in songs["tracks"]["items"]:
                id = track['id']
                features = sp.audio_features(id)
                if(features):
                    print(features)
                    removed = remove_features(audio_f, features[0])
                    audio_features.append(removed)

    return audio_features

def getRandomSearch():
    characters = 'abcdefghijklmnopqrstuvwxyz'
    index = random.randint(0, 25)
    return characters[index] + '%'

def remove_features(features, item):
    ret = {}
    for feature in features:
        ret[feature] = item[feature]
    return ret

def get_songs_from_user(audio_f, uid):
    playlists = sp.user_playlists(uid)
    audio_features = []
    while playlists:
        print("Playlist names: ")
        for i, playlist in enumerate(playlists['items']):
            tracks = sp.playlist_tracks(playlist['id'])
            print(playlist["name"])
            if tracks:
                for _, track in enumerate(tracks['items']):
                    id = track['track']['id']
                    features = sp.audio_features(id)
                    if features:
                        removed = remove_features(audio_f, features[0])
                        audio_features.append(removed)

    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
    print('Songs from user {} have been added'.format(uid))
    return audio_features

def setup():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    cc_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=cc_manager)

if __name__ == '__main__':
    sp = setup()

    song_attributes = ('album', 'track_number', 'id', 'name', 'uri', 'acousticness', 'danceability',
                       'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
                       'valence', 'popularity')

    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

    df_user = pd.DataFrame(get_songs_from_user(features, 'jeremyhsu1'))
    n_user_songs = len(df_user.index)
    user_labels = np.ones(n_user_songs)

    df_random = pd.DataFrame(getRandomSongs(features))
    n_random_songs = len(df_random.index)
    random_labels = np.zeros(n_random_songs)
    labels = np.append(user_labels, random_labels)
    print(labels)


    print(df_random)
    print(df_user)
    # print(getRandomSearch())

    df_user = df_user.append(df_random, ignore_index=True)

    print(df_user)

    forest = RandomForestClassifier()

    kmeans = KMeans()

    kmeans_params = {
        "n_clusters": np.arange(2, 10, 1),
        "n_init": np.arange(10, 15, 1),
    }
    forest_params = {
        "n_estimators": np.arange(10, 200, 10),
        "min_samples_leaf": np.arange(1, 100, 10),
        "max_features": ['auto', 'sqrt', 'log2']
    }
    clf = GridSearchCV(forest, forest_params)

    kmeans_clf = GridSearchCV(kmeans, kmeans_params)
    kmeans_clf.fit(df_user)
    print(kmeans_clf.best_params_)
    clf.fit(df_user, labels)
    print(clf.best_params_)

    modelpath = os.path.join(os.getcwd(), 'model_files')
    if not os.path.exists(modelpath):
        os.makedirs(modelpath)
    joblib.dump(clf, os.path.join(modelpath, 'spotify.joblib'))
    joblib.dump(kmeans_clf, os.path.join(modelpath, 'spotify_kmeans.joblib'))