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
pickle.dump(replay_list, open('parsed_replays.SC2Replay', 'wb'))

#generate timeline as dataframe and save as csv
for matchup, matchup_replays in replay_list.items():
    games_data=matchup_replays
    train_file_name='data/'+str(matchup)+'_train.csv'
    games_data=games_data.fillna(0)
    games_data.to_csv(train_file_name)

pvp_data=replay_list['pvp']
pvp_features=training_features.pvp
columns_bool=pvp_data.columns.isin(pvp_features)
pvp_data_filter=pvp_data.loc[:, columns_bool]
pvp_data_filter.to_csv('pvp_train.csv')

pvt_data=pd.read_csv('data/pvt_train.csv', index_col=0)
pvt_features=training_features.pvt
columns_bool=pvt_data.columns.isin(pvp_features)
pvt_data_filter=pvt_data.loc[:, columns_bool]
#pvt_data_filter.iloc[:, 0:8]=np.log(pvt_data_filter.iloc[:, 0:8]+1)
pvt_data_filter.to_csv('pvt_train.csv')

#RFC model for each matchup

for matchup in replay_list.keys():
    data_path='data/'+str(matchup)+'_train.csv'
    games=pd.read_csv(data_path)
    try:
        games["result"] = games["result"].astype(int)
        features = games.drop('result', axis=1)
        results = games['result']

        # implementing train-test-split, not required for applying the model
        #X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=66)

        # random forest model creation
        rfc = ensemble.RandomForestClassifier(n_estimators=1500, n_jobs=-1)
        rfc.fit(features,results)
        filename='models/rfc_'+str(matchup)+'.model'
        pickle.dump(rfc, open(filename, 'wb'))
    except KeyError:
        pass

games=pd.read_csv('pvp_train.csv', index_col=0).fillna(0)
games.loc[:,"result"] = games["result"].astype(int)
features = games.drop('result', axis=1)
results = games['result']
rfc = ensemble.RandomForestClassifier(n_estimators=1500, n_jobs=-1, class_weight='balanced', max_features='sqrt')
rfc.fit(features,results)
filename='pvp_test.model'
pickle.dump(rfc, open(filename, 'wb'))

games=pd.read_csv('pvt_train.csv', index_col=0).fillna(0)
games.loc[:,"result"] = games["result"].astype(int)
features = games.drop('result', axis=1)
results = games['result']
rfc = ensemble.RandomForestClassifier(n_estimators=1500, n_jobs=-1, class_weight='balanced', max_features='sqrt')
rfc.fit(features,results)
filename='D:/sc2models/pvt_test.model'
pickle.dump(rfc, open(filename, 'wb'))

logit = linear_model.LogisticRegression(penalty='l2', n_jobs=-1)
logit.fit(features,results)
pickle.dump(logit, open('D:/sc2models/pvt_test_logit.model', 'wb'))

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

features_interactions=make_interactions(features, 'loop')

logit_interactions = linear_model.LogisticRegression(penalty='l2', n_jobs=-1, max_iter=250)
logit_interactions.fit(features_interactions,results)
pickle.dump([logit_interactions,features_interactions.columns], open('D:/sc2models/pvt_test_logit_w_interactions.model', 'wb'))

# X_interactions will have additional features representing the interactions
print(X_interactions)

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