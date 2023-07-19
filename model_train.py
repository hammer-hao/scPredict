import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn import ensemble
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import replay
import training_features
import pickle
from pathlib import Path
import os
from dotenv import load_dotenv
import tqdm
import numpy as np

load_dotenv()
replay_folder=os.getenv('PATHTOREPLAY')
replays = Path(replay_folder)

replay_list = replay.recursereplays(replays)

#save parsed replays
with open('D:/sc2models/parsed_replays', 'wb') as file:
    pickle.dump(replay_list, file)

with open('D:/sc2models/parsed_replays', 'rb') as file:
    replay_list = pickle.load(file)

features={
    'pvp':training_features.pvp,
    'pvz':training_features.pvz,
    'pvt':training_features.pvt,
    'zvt':training_features.zvt,
    'tvt':training_features.tvt,
    'zvz':training_features.zvz
}

#generate timeline as dataframe and save as csv
for matchup, matchup_replays in replay_list.items():
    matchup_features=features[matchup]
    columns_bool=matchup_replays.columns.isin(matchup_features)
    filtered_data=matchup_replays.loc[:,columns_bool]
    train_file_name='data/'+str(matchup)+'_train.csv'
    filtered_data.to_csv(train_file_name)

#interact all variables with gameloop
def make_interactions(df, root):
    feature = root
    specific_feature = df[root]
    interaction_terms = pd.DataFrame()
    for column in df.columns:
        if column != feature:
            interaction_term = specific_feature * df[column]  # Create the interaction term
            interaction_terms[column+'_interaction'] = interaction_term# Reshape and append to the list
    X_interactions = pd.concat([df, interaction_terms], axis=1)
    return X_interactions

for matchup in ['pvp', 'pvz', 'pvt', 'zvt', 'zvz', 'tvt']:
    data_path='data/'+matchup+'_train.csv'
    games=pd.read_csv(data_path, index_col=0).fillna(0)
    games.loc[:,"result"] = games["result"].astype(int)
    features = games.drop('result', axis=1)
    results = games['result']

    #logit
    logit = linear_model.LogisticRegression(penalty='l2', n_jobs=-1)
    logit.fit(features,results)
    savepath='models/'+matchup+'_logit.model'
    pickle.dump(logit, open(savepath, 'wb'))

    #logit with interactions
    features_interactions=make_interactions(features, 'loop')
    logit_interactions = linear_model.LogisticRegression(penalty='l2', n_jobs=-1, max_iter=250)
    logit_interactions.fit(features_interactions,results)
    savepath_temporal='models/'+matchup+'_logit_temporal.model'
    pickle.dump([logit_interactions,features_interactions.columns], open(savepath_temporal, 'wb'))

# predictions
rfc_predict = rfc.predict(X_test)

rfc_cv_score = cross_val_score(rfc, x, y, cv=10, scoring='roc_auc')

print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, rfc_predict))
print('\n')
print("=== Classification Report ===")
print(classification_report(y_test, rfc_predict))
print('\n')
print("=== All AUC Scores ===")
print(rfc_cv_score)
print('\n')
print("=== Mean AUC Score ===")
print("Mean AUC Score - Random Forest: ", rfc_cv_score.mean())

filename='rfc_pvz.model'
pickle.dump(rfc, open(filename, 'wb'))