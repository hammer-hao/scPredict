from scpredict.parsing import ZGameParser
from scpredict.settings import *
import pandas as pd
import pickle
from dotenv import load_dotenv
import os
import warnings

class Predictor():
    def __init__(self):
        load_dotenv()
        self.model_path = os.environ.get('PATHTOMODELS')
        self.models = {}
        self.matchups = matchups
        self.parser = ZGameParser()

        with open(f'{self.model_path}/feature_names.pkl', 'rb') as f:
            self.feature_names = pickle.load(f)

        for matchup in self.matchups:
            with open(f'{self.model_path}/{matchup}.pkl', 'rb') as f:
                self.models[matchup] = pickle.load(f)
        
    def predict(self, path_to_replay):
        timeline, matchup, name_1, name_2 = self.parser.parse(path=path_to_replay)
        prediction_features = pd.DataFrame(columns=self.feature_names[matchup])
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            for entry in timeline:
                row = {feature: entry.get(feature, None) for feature in self.feature_names[matchup]}
                prediction_features = prediction_features.append(row, ignore_index=True)
        prediction_features = prediction_features.fillna(0)
        logit_predictions = self.models[matchup].predict_proba(prediction_features)[:, -1]
        self.parser.reset()
        return logit_predictions, name_1, name_2