#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
import spotipy
import pandas as pd
from flask import Flask
from flask import redirect
from flask import request
from flask import jsonify
from flask import session
from flask_celery import make_celery
sys.path.append('spotify_model')
from spotify_model.original_model import setup
from spotify_model.original_model import remove_features
from spotify_model.spotify_predict import SpotifyModel


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_BACKEND'] = 'redis://localhost:6379/0'
celery = make_celery(app)

SSK = None
CLI_ID = os.environ['CLIENT_ID']
CLI_SEC = os.environ['CLIENT_SECRET']

app.secret_key = os.urandom(12) # Need to read about Flask secret keys later

API_BASE = 'https://accounts.spotify.com'
REDIRECT_URI = 'http://127.0.0.1:5000/api_callback'
SCOPE = 'playlist-read-private,playlist-read-collaborative'
SHOW_DIALOG = True # Set to False when in production

@app.route('/login')
def verify():
    auth_url = '{}/authorize?client_id={}&response_type=code&redirect_uri={}&scope={}&show_dialog={}'.format(API_BASE, CLI_ID, REDIRECT_URI, SCOPE, SHOW_DIALOG)
    print(auth_url)
    return redirect(auth_url)

@app.route('/index', methods=['GET'])
def index():
    return 'Index from server'

@app.route('/api_callback')
def api_callback():
    session.clear()
    code = request.args.get('code')

    auth_token_url = API_BASE + '/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLI_ID,
        'client_secret': CLI_SEC
    }
    response = requests.post(auth_token_url, data=data)
    body = response.json()
    session['token'] = body.get('access_token')
    # return redirect('/get_profile_info')
    return redirect('http://localhost:3000/')

@app.route('/get_profile_info', methods=['GET'])
def get_profile_info():
    if 'token' not in session:
        return redirect('/login')
    sp = spotipy.Spotify(auth=session['token'])
    response = sp.current_user()
    return response

@app.route('/go', methods=['GET'])
def go():
    if 'token' not in session:
        return redirect('/login')
    sp = spotipy.Spotify(auth=session['token'])
    response = sp.current_user()
    if 'id' not in response:
        return 'Id not found. May need to add scopes'
    print(response['id'])
    print(sp.user_playlists(response['id']))
    return 'Go'

# Process multiple songs
@app.route('/make_predictions', methods=['POST'])
def make_predictions():
    # Should probably check if songs are empty in here as well
    songs = request.get_json()['songs']
    task = predict.delay(songs)
    return jsonify({'task_id': task.task_id})

@app.route('/check/<task_id>')
def check(task_id):
    result = celery.AsyncResult(task_id)
    print(result.status)
    if result.status == 'PENDING' or result.status == 'FAILURE':
        return result.status
    return result.get()

# Predict multiple songs
@celery.task(name='app.predict')
def predict(songs):
    sp = setup()
    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness',
                'tempo', 'valence']
    sp_model = SpotifyModel()
    predictions = {}
    for song_name in songs:
        song = sp.search(song_name, limit=1, offset=0)
        audio_features = []
        if song:
            # Should probably include approximate song name there too
            track = song['tracks']['items'][0]
            song_features = sp.audio_features(track['id'])
            if song_features:
                removed = remove_features(features, song_features[0])
                audio_features.append(removed)
            print('')
            predictions[song_name] = sp_model.predict(audio_features)
        else:
            predictions[song_name] = 'Could not find a matching song'
    return json.dumps(predictions)
