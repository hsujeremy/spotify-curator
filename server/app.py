#!/usr/bin/env python3
import os
import json
import time
import requests
import spotipy
from flask import Flask
from flask import redirect
from flask import request
from flask import jsonify
from flask import session
from flask import make_response


app = Flask(__name__)

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

@app.route('/index')
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
    return redirect('http://localhost:3000/')

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
