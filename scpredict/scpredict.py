from scpredict.parsing import ZGameParser
from scpredict.settings import *
import pandas as pd
import pickle
from dotenv import load_dotenv
import os
import shap
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class Predictor():
    def __init__(self):
        load_dotenv()
        self.model_path = os.environ.get('PATHTOMODELS')
        self.explainer_path = os.environ.get('PATHTOEXPLAINERS')
        self.path_to_pca = os.environ.get('PATHTOPCA')
        self.models = {}
        self.matchups = matchups
        self.parser = ZGameParser()
        self.explainers = {}
        self.pca_scalors = {}
        self.pca_transformed_data = {}
        self.pca = {}

        with open(f'{self.model_path}/feature_names.pkl', 'rb') as f:
            self.feature_names = pickle.load(f)

        for matchup in self.matchups:
            with open(f'{self.model_path}/{matchup}.pkl', 'rb') as f:
                self.models[matchup] = pickle.load(f)
            with open(f'{self.explainer_path}/{matchup}_shap.pkl', 'rb') as f:
                self.explainers[matchup] = pickle.load(f)
            with open(f'{self.path_to_pca}/scalor/{matchup}_scalor.pkl', 'rb') as f:
                self.pca_scalors[matchup] = pickle.load(f)
            with open(f'{self.path_to_pca}/pca/{matchup}_pca.pkl', 'rb') as f:
                self.pca[matchup] = pickle.load(f)
            with open(f'{self.path_to_pca}/data/{matchup}_transformed_data.pkl', 'rb') as f:
                self.pca_transformed_data[matchup] = pickle.load(f)

    def predict(self, path_to_replay):
        timeline, matchup, name_1, name_2 = self.parser.parse(path=path_to_replay)
        features = self.feature_names[matchup]
        rows = [{feature: entry.get(feature, 0) for feature in features} for entry in timeline]
        
        prediction_features = pd.DataFrame(rows, columns=features).fillna(0)
        logit_predictions = self.models[matchup].predict_proba(prediction_features)[:, -1]
        
        self.parser.reset()
        return logit_predictions, name_1, name_2

    
    def get_shap(self, path_to_replay):
        timeline, matchup, name_1, name_2 = self.parser.parse(path=path_to_replay)
        features = self.feature_names[matchup]
        explainer = self.explainers[matchup]
        rows = [{feature: entry.get(feature, 0) for feature in features} for entry in timeline]

        prediction_features = pd.DataFrame(rows, columns=features).fillna(0)
        shap_values = explainer(prediction_features)

        mean_abs_shap_values = np.mean(np.abs(shap_values.values), axis=0)
        feature_importance = pd.DataFrame({
            'Feature': prediction_features.columns,
            'Mean Absolute SHAP Value': mean_abs_shap_values
        }).sort_values(by='Mean Absolute SHAP Value', ascending=False)

        return shap_values, feature_importance
