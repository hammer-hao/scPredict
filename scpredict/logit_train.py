from sklearn.linear_model import LogisticRegression
import pandas as pd
from settings import *
import pickle
from dotenv import load_dotenv
import os
import shap

load_dotenv()
model_path = os.environ.get('PATHTOMODELS')

def train_all():
    feature_names = {}
    for matchup in matchups:
        matchup_df = pd.read_csv(f'replays_processed/zephyrus/{matchup}.csv')
        features = matchup_df.drop(['winner'], axis=1).fillna(0)
        labels = 2-matchup_df['winner']
        logisticRegr = LogisticRegression(max_iter=5000)
        logisticRegr.fit(features, labels)
        with open(f'{model_path}/{matchup}.pkl', 'wb') as f:
            pickle.dump(logisticRegr, f)
        feature_names[matchup]=(list(features.columns))
    with open(f'{model_path}/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)


def generate_explainers():
    for matchup in matchups:
        data_path = f'replays_processed/zephyrus/{matchup}.csv'
        matchup_data = pd.read_csv(data_path).fillna(0).drop(['winner'], axis=1)
        model_path = f'saved_models/logit/{matchup}.pkl'
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        explainer = shap.Explainer(model, matchup_data)
        shap_path = f'saved_models/shap/{matchup}_shap.pkl'
        with open(shap_path, 'wb') as f:
            pickle.dump(explainer, f)

if __name__ == "__main__":
    train_all()
    generate_explainers()