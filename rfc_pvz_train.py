import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn import ensemble
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
import replay
import pickle
from pathlib import Path
from zephyrus_sc2_parser import parse_replay
import tqdm

replays = Path('replays_raw')
replay_list = replay.recursereplays(replays)

totalunits=[]
for thisreplay in tqdm.tqdm(replay_list):
    totalunits+=replay.gen_total_timeline(thisreplay)

pvz_games = pd.DataFrame(totalunits)
pvz_games.to_csv('pvz_train.csv')
pvz_games = pvz_games.fillna(0)

pvz_games["Protosswin"] = pvz_games["Protosswin"].astype(int)
x = pvz_games.drop('Protosswin', axis=1)
y = pvz_games['Protosswin']

# implementing train-test-split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=66)


# random forest model creation
rfc = ensemble.RandomForestClassifier()
rfc.fit(X_train,y_train)
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