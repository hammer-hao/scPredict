from sklearn.linear_model import LogisticRegression
import pandas as pd
from scpredict.settings import *
import pickle
from dotenv import load_dotenv
import os

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

if __name__ == "__main__":
    train_all()