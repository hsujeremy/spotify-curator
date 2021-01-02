# Spotify-Curator

An (eventual) web application that uses machine learning to determine the probability one would like a song based on their previously liked songs.

## Getting Started

### Server-Side
The server is written in Python and uses Flask. We call the Spotify Web API here. To install required packages at this moment, navigate to root project directory and run:
```
pip(3) install -r requirements.txt
```
To start the server, you need to first set environment variables for the Flask app, Spotify CLIENT_ID, and Spotify CLIENT_SECRET:
```
cd server
export FLASK_APP={path to}/app.py
export CLIENT_ID={your client ID}
export CLIENT_SECRET={your client secret}
flask run
```

### Client-Side
The client is written in JavaScript with React. To install required dependencies, navigate into the `client` directory and run:
```
npm install
```
Once the server is running, you can start your app with:
```
yarn start
```
