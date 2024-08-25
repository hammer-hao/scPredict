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
from scipy.spatial.distance import cdist

class Predictor():
    def __init__(self):

        print('initializing predictor...')

        load_dotenv()
        self.model_path = os.environ.get('PATHTOMODELS')
        self.explainer_path = os.environ.get('PATHTOEXPLAINERS')
        self.path_to_pca = os.environ.get('PATHTOPCA')
        self.path_to_data = os.environ.get('PATHTOREFERENCES')
        self.models = {}
        self.matchups = matchups
        self.parser = ZGameParser()
        self.explainers = {}
        self.pca_scalors = {}
        self.pca_transformed_data = {}
        self.pca = {}
        self.matchup_df = {}

        print('initialization complete. Loading local files...')

        with open(f'saved_models/pca/feature_names_pca.pkl', 'rb') as f:
            self.feature_names = pickle.load(f)

        with open(f'{self.model_path}/feature_names.pkl', 'rb') as f:
            self.features_predict = pickle.load(f)

        for matchup in self.matchups:

            print(f'loading file for {matchup}...')

            with open(f'{self.model_path}/{matchup}.pkl', 'rb') as f:
                print('loading model file...')
                self.models[matchup] = pickle.load(f)
            #with open(f'{self.explainer_path}/{matchup}_shap.pkl', 'rb') as f:
            #    print('loading shap explainer...')
            #    self.explainers[matchup] = pickle.load(f)
            with open(f'{self.path_to_pca}/scalor/{matchup}_scalor.pkl', 'rb') as f:
                print('loading pca scalor...')
                self.pca_scalors[matchup] = pickle.load(f)
            with open(f'{self.path_to_pca}/pca/{matchup}_pca.pkl', 'rb') as f:
                print('loading pca transformation...')
                self.pca[matchup] = pickle.load(f)
            with open(f'{self.path_to_pca}/data/{matchup}_transformed_data.pkl', 'rb') as f:
                print('loading transformed pca data...')
                self.pca_transformed_data[matchup] = pd.DataFrame(data=pickle.load(f), columns=[f'PC{i+1}' for i in range(50)])
            print('loading all replays...')
            self.matchup_df[matchup] = pd.read_csv(f'{self.path_to_data}/{matchup}.csv')

    def predict(self, path_to_replay):
        timeline, matchup, name_1, name_2 = self.parser.parse(path=path_to_replay)
        f_names = self.features_predict[matchup]
        rows = [{feature: entry.get(feature, 0) for feature in f_names} for entry in timeline]
        
        prediction_features = pd.DataFrame(rows, columns=f_names).fillna(0)
        logit_predictions = self.models[matchup].predict_proba(prediction_features)[:, -1]
        
        self.parser.reset()
        return logit_predictions, name_1, name_2

    def get_pca(self, path_to_replay, timestamp=1, N=3):

        parser = ZGameParser()
        timeline, matchup, name_1, name_2 = parser.parse(path=path_to_replay)

        reference_data = self.matchup_df[matchup]

        f_names = self.feature_names[matchup]
        rows = [{feature: entry.get(feature, 0) for feature in f_names} for entry in timeline]
        prediction_features = pd.DataFrame(rows, columns=f_names).fillna(0)
        prediction_features = self.pca_scalors[matchup].transform(prediction_features)
        query_point = self.pca[matchup].transform(prediction_features)[timestamp,:].reshape(1, -1)

        distances = cdist(query_point, self.pca_transformed_data[matchup], metric='cosine').flatten()
        sorted_distances = pd.DataFrame({'index':self.pca_transformed_data[matchup].index, 'distance': distances}).sort_values(by='distance')

        top_similar_indices = sorted_distances['index'].head(N).values
        results = reference_data.iloc[top_similar_indices,:].drop_duplicates(subset='file_name', keep='first')
        names = results['file_name'].tolist()
        timestamps = results['gameloop'].tolist()
        
        return names, timestamps

'''  
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
'''