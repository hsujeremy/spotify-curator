# ML-Enabled Spotify Curator

**Authors**: Jeremy Hsu and Steve Li

Spotify Curator is a full-stack web application leveraging machine learning to
help Spotify users discover new songs they love.

## Approach and Data Analysis
Our main dataset consists of songs included in a given user's playlist, labeled
as songs that they user "likes," and a relatively equal set of random songs
labeled as songs that the user "dislikes." For each song, we take a look at
several audio features using the Spotify API, mainly
* Acousticness
* Danceability
* Energy
* Instrumentalness
* Liveness
* Loudness
* Speechiness
* Tempo
* Valence

Each value is a number between 0 and 1, therefore they can easily be transferred
and put into a supervised classification model. With some research, we settled on
a Random Foest Classifier, using GridSearchV with the parameters:

```
forest_params = {
    'n_estimators': np.arange(10, 200, 10),
    'min_samples_leaf': np.arange(1, 100, 10),
    'max_features': ['auto', 'sqrt', 'log2']
}
```
Approaches can obviously be improved with accurate data, if a user for example
has a playlist of songs that has their dislikes. Furthermore, an unsupervised
model such as kmeans could be used to determine the specific genre or subset a
given song falls within, and using a simple linear classifier within that subset
of data to determine whether that given song falls within an acceptable range in
that genre.

## Architecture Overview

The backend server is written in Python and uses Flask. We call the Spotify Web
API here. To deploy the models, we process long running tasks using a
distributed task queue. We use Celery as the queue with Redis currently serving
as both the message broker and the Celery backend.

The frontend client is written in JavaScript using the React framework.

## Contributing

### Backend Setup

We recommend using a virtual environment. To create one, run:
```
python3 -m venv venv
source venv/bin/activate
```
And to install depedencies:
```
pip(3) install -r requirements.txt
```
You also need to first set environment variables for the Flask app, Spotify CLIENT_ID, and Spotify CLIENT_SECRET:
```
export FLASK_APP={path to}/app.py
export CLIENT_ID={your client ID}
export CLIENT_SECRET={your client secret}
```
For everything to work as intended, there should be at least 3 servers running
in total (1 Flask, 1 Redis, and 1-16 Celery workers).
```
redis-server
celery -A app.celery worker --loglevel=info
flask run
```

### Frontend Setup

The client is written in JavaScript with React. You can install required
dependencies with:
```
npm install
```
Once the server is running, you can start your app with:
```
yarn start
```
