from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from settings import *
import pickle

def train_all():
    feature_names = []
    for matchup in matchups:
        matchup_df = pd.read_csv(f'replays_processed/zephyrus/{matchup}.csv')
        features = matchup_df.drop(['winner'], axis=1).fillna(0)
        labels = 2-matchup_df['winner']
        logisticRegr = LogisticRegression(max_iter=5000)
        logisticRegr.fit(features, labels)
        with open(f'saved_models/logit/{matchup}.pkl', 'wb') as f:
            pickle.dump(logisticRegr, f)
        feature_names.append(list(features.columns))
    with open('saved_models/logit/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)

if __name__ == "__main__":
    train_all()