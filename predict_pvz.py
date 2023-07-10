from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn import ensemble
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import replay
from zephyrus_sc2_parser import parse_replay
import pandas as pd
import training_features
import matplotlib.pyplot as plt

file = open('pvp_test.model','rb')
pvz_rfc=pickle.load(file)
file.close()

df_dict={}
for feature in training_features.pvp:
    df_dict.update({feature:0})

def predict_game(game):
    thisreplay=parse_replay(game)
    totallist=[df_dict]+replay.gen_total_timeline(thisreplay, 'pvp')
    timeline=pd.DataFrame(totallist).drop(['result'], axis=1).fillna(0)
    predictions = pvz_rfc.predict_proba(timeline)
    winratearr = [(1-percentage[0]) for percentage in predictions]
    return winratearr, timeline

test, game_details=predict_game('Altitude LE (9).SC2Replay')
fig= plt.plot(test)
plt.xlabel('time')
plt.ylabel('winrate')
plt.title('win rate in real time')
plt.savefig('winrate.png')