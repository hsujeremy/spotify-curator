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

### Approach and Data Analysis 
Our main dataset consists of songs included in a given user's playlist, labeled as songs that they user "likes," and a relatively equal set of random songs labeled as songs that the user "dislikes." For each song, we take a look at several audio features using the Spotify api, mainly 
```
['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness',
                'tempo', 'valence']
```
Each value is a number between 0 and 1, therefore they can easily be transferred and put into a supervised classification model. With some research we settled on a Random Foest Classifier, using GridSearchV with the params:

```
forest_params = {
        'n_estimators': np.arange(10, 200, 10),
        'min_samples_leaf': np.arange(1, 100, 10),
        'max_features': ['auto', 'sqrt', 'log2']
    }
```
Approaches can obviously be improved with accurate data, if a user for example has a playlist of songs that has their dislikes. Furthermore, an unsupervised model such as kmeans could be used to determine the specific genre or subset a given song falls within, and using a simple linear classifier within that subset of data to determine whether that given song falls within an acceptable range in that genre. 


### Client-Side
The client is written in JavaScript with React. To install required dependencies, navigate into the `client` directory and run:
```
npm install
```
Once the server is running, you can start your app with:
```
yarn start
```
