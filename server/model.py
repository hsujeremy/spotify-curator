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
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV


def get_random_songs(sp, audio_f):
    def get_random_search():
        characters = 'abcdefghijklmnopqrstuvwxyz'
        i = random.randint(0, 25)
        return characters[i] + '%'

    audio_features = []

    for i in range(10):
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

def get_songs_from_user(sp, audio_f, userid):
    playlists = sp.user_playlists(userid)
    audio_features = []

    while True:
        print('Playlist names:')
        for i, playlist in enumerate(playlists['items']):
            tracks = sp.playlist_tracks(playlist['id'])
            print(playlist['name'])
            if tracks:
                for j, track in enumerate(tracks['items']):
                    id = track['track']['id']
                    features = sp.audio_features(id)
                    if features:
                        removed = remove_features(audio_f, features[0])
                        audio_features.append(removed)

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break

    print('Songs from user {} have been added'.format(userid))
    return audio_features

def setup():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    cc_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=cc_manager)

def train(sp, userid):
    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

    # Prepare data
    df_user = pd.DataFrame(get_songs_from_user(sp, features, userid))
    n_user_songs = len(df_user.index)
    user_labels = np.ones(n_user_songs)

    df_random = pd.DataFrame(get_random_songs(sp, features))
    n_random_songs = len(df_random.index)
    random_labels = np.zeros(n_random_songs)
    labels = np.append(user_labels, random_labels)
    print(labels)

    print(df_random)
    print(df_user)

    df_user = df_user.append(df_random, ignore_index=True)
    print(df_user)

    # Perform training
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
    clf.fit(df_user, labels)
    print(clf.best_params_)

    kmeans_clf = GridSearchCV(kmeans, kmeans_params)
    kmeans_clf.fit(df_user)
    print(kmeans_clf.best_params_)

    return clf, kmeans_clf

def remove_features(features, item):
    ret = {}
    for feature in features:
        ret[feature] = item[feature]
    return ret

def evaluate(sp, clf, kmeans_clf, song):
    song_attributes = ('album', 'track_number', 'id', 'name', 'uri', 'acousticness', 'danceability',
                       'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
                       'valence', 'popularity')
    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

    songs = sp.search(song, limit=1, offset=0)
    audio_features = []

    if songs:
        for track in songs['tracks']['items']:
            print(track)
            features = sp.audio_features(track['id'])
            if features:
                removed = remove_features(audio_f, features[0])
                audio_features.append(removed)

    df_song = pd.DataFrame(audio_features)
    print(clf.classes_)
    prediction = clf.predict_proba(df_song)
    kmeans_prediction = kmeans_clf.predict(df_song)
    return prediction, kmeans_prediction

def main():
    sp = setup()

    # Prepare data

    clf, kmeans_clf = train_model(sp, '12176195123')

    for song in ('Do Not Wait', 'Are You Bored Yet?'):
        predictions = evaluate(sp, clf, kmeans_clf, 'Do Not Wait')
        print('FINAL PREDICTIONS:', predictions)

if __name__ == '__main__':
    main()
