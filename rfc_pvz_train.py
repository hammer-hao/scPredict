import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn import ensemble
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import replay
import pickle
from pathlib import Path
from zephyrus_sc2_parser import parse_replay
import os
from dotenv import load_dotenv
import tqdm

load_dotenv()
replay_folder=os.getenv('PATHTOREPLAY')
replays = Path(replay_folder)
replay_list = replay.recursereplays(replays)

#save parsed replays
pickle.dump(replay_list, open('parsed_replays', 'wb'))

#generate timeline as dataframe and save as csv
for matchup, matchup_replays in replay_list.items():
    totalunits=[]
    for thisreplay in tqdm.tqdm(matchup_replays):
        totalunits+=replay.gen_total_timeline(thisreplay, matchup)
    games_data=pd.DataFrame(totalunits)
    train_file_name='data/'+str(matchup)+'_train.csv'
    games_data=games_data.fillna(0)
    games_data.to_csv(train_file_name)

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
        rfc = ensemble.RandomForestClassifier()
        rfc.fit(features,results)
        filename='models/rfc_'+str(matchup)+'.model'
        pickle.dump(rfc, open(filename, 'wb'))
    except KeyError:
        pass

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