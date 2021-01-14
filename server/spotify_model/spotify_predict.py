#!/usr/bin/env python3
import os
import joblib
import pandas as pd
from schema import Schema
from ml_model_abc import MLModel


class SpotifyModel(MLModel):
    input_schema = Schema([{
        'acousticness': float,
        'danceability': float,
        'energy': float,
        'instrumentalness': float,
        'liveness': float,
        'loudness': float,
        'speechiness': float,
        'tempo': float,
        'valence': float
    }])

    output_schema = Schema({
        'prediction': float,
        'kmeans_prediction': float
    })

    def __init__(self):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        # Assumes that models are already loaded
        self.clf = joblib.load(os.path.join(dirpath, 'model_files', 'spotify.joblib'))
        self.kmeans_clf = joblib.load(os.path.join(dirpath, 'model_files', 'spotify_kmeans.joblib'))

    def predict(self, data):
        # Call super method to validate data against input_schema
        super().predict(data=data)

        # Assume data is in the form of audio_features array in original file
        df_song = pd.DataFrame(data)
        prediction = self.clf.predict_proba(df_song)
        kmeans_prediction = self.kmeans_clf.predict(df_song)
        result = {'prediction': float(prediction[0][1]), 'kmeans_prediction': float(kmeans_prediction[0])}
        self.output_schema.validate(result)
        return result
