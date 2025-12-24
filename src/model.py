import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StandardScaler
import pickle
import os

class SongPopularityPredictor:

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_coloumns = ['danceability', 'energy', 'key', 'loudness', 'mode',
                                 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                                 'valence', 'tempo', 'duration_ms', 'time_signature']
        self.feature_importance = None
    
    def prepare_data(self, high_pop_df, low_pop_df):
        high_pop_df['label'] = 1
        low_pop_df['label'] = 0

        combined_df = pd.concat([high_pop_df, low_pop_df], ignore_index=True)

        X = combined_df[self.feature_columns]
        y = combined_df['label']

        return X, y
    
    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train_scaled = self.scalar.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model = RandomeForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)

        train_accuracy = self.model.score(X_train_scaled, y_train)
        test_accuracy = self.model.score(X_test_scaled, y_test)

        self.feature_importance = pd.DataFrame({
            'feature':self.feature_columns,
            'importance': self.model.feature_importances_}).sort_values('importance', ascending=False)
        return train_accuracy, test_accuracy
        
    def predict(self, song_features):

        features_df=pd.DataFrame([song_features])
        features_ordered = features_df[self.features_columns]

        features_scaled = self.scaler.transform(features_ordered)

        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]

        return prediction, probability
    
    def get_feature_importance_dict(self):
        if self.feature_importance is not None:
            return dict(zip(
                self.feature_imoportance['feature'],
                self.feature_importance['importance']
            ))
        return None