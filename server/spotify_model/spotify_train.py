#!/usr/bin/env python3
import os
import random
import spotipy
import time
import joblib
import numpy as np
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV


def get_random_songs(sp, audio_f):
    audio_features = []

    for i in range(200):
        offset = random.randint(0, 500)
        print(offset)

        query = get_random_search()
        print(query)
        songs = sp.search(query, limit=10, offset=offset)
        if songs:
            for track in songs['tracks']['items']:
                id = track['id']
                features = sp.audio_features(id)
                if features:
                    print(features)
                    removed = remove_features(audio_f, features[0])
                    audio_features.append(removed)

    return audio_features

def get_random_search():
    characters = 'abcdefghijklmnopqrstuvwxyz'
    index = random.randint(0, 25)
    return characters[index] + '%'

def remove_features(features, item):
    ret = {}
    for feature in features:
        ret[feature] = item[feature]
    return ret

def get_songs_from_user(sp, audio_f, uid):
    playlists = sp.user_playlists(uid)
    audio_features = []

    # import json
    # with open('playlists.json', 'w') as fout:
    #     json.dump(playlists, fout, indent=4)

    while playlists:
        print('Playlist names:')
        for i, playlist in enumerate(playlists['items']):
            print(playlist['name'])
            tracks = sp.playlist_tracks(playlist['id'])
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
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    cc_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=cc_manager)

def train():
    sp = setup()

    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness',
                'tempo', 'valence']

    df_user = pd.DataFrame(get_songs_from_user(sp, features, 'jeremyhsu1'))
    n_user_songs = len(df_user.index)
    user_labels = np.ones(n_user_songs)

    df_random = pd.DataFrame(get_random_songs(sp, features))
    n_random_songs = len(df_random.index)
    random_labels = np.zeros(n_random_songs)
    labels = np.append(user_labels, random_labels)
    print(labels)

    print(df_random)
    print(df_user)
    # print(get_random_search())
    df_user = df_user.append(df_random, ignore_index=True)
    print(df_user)

    forest = RandomForestClassifier()
    forest_params = {
        'n_estimators': np.arange(10, 200, 10),
        'min_samples_leaf': np.arange(1, 100, 10),
        'max_features': ['auto', 'sqrt', 'log2']
    }

    kmeans = KMeans()
    kmeans_params = {
        'n_clusters': np.arange(2, 10, 1),
        'n_init': np.arange(10, 15, 1),
    }
    clf = GridSearchCV(forest, forest_params)

    kmeans_clf = GridSearchCV(kmeans, kmeans_params)
    kmeans_clf.fit(df_user)
    print(kmeans_clf.best_params_)
    clf.fit(df_user, labels)
    print(clf.best_params_)

    dirpath = os.path.dirname(os.path.realpath(__file__))
    modelpath = os.path.join(dirpath, 'model_files')
    if not os.path.exists(modelpath):
        os.makedirs(modelpath)
    joblib.dump(clf, os.path.join(modelpath, 'spotify.joblib'))
    joblib.dump(kmeans_clf, os.path.join(modelpath, 'spotify_kmeans.joblib'))
    print('Training complete')
