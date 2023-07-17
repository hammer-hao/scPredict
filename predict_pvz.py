import pickle
import replay
from zephyrus_sc2_parser import parse_replay
import pandas as pd
import training_features
import matplotlib.pyplot as plt

file = open('D:/sc2models/pvt_test_logit.model','rb')
pvt_logit=pickle.load(file)
file.close()

file = open('D:/sc2models/pvt_test_logit_w_interactions.model','rb')
pvt_logitint=pickle.load(file)
file.close()

df_dict={}
for feature in training_features.pvt:
    df_dict.update({feature:0})

def predict_game(game, model):
    thisreplay=parse_replay(game, local=True, tick=90)
    totallist=[df_dict]+replay.gen_total_timeline(thisreplay, 'pvt')
    timeline=pd.DataFrame(totallist).drop(['result'], axis=1).fillna(0)
    predictions = model.predict_proba(timeline)
    winratearr = [(1-percentage[0]) for percentage in predictions]
    return winratearr, timeline

pvt_logit=pickle.load(file)

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

def predict_with_int(game, model):
    thisreplay=parse_replay(game, local=True, tick=90)
    totallist=[df_dict]+replay.gen_total_timeline(thisreplay, 'pvt')
    timeline=pd.DataFrame(totallist).drop(['result'], axis=1).fillna(0)
    timeline_int=make_interactions(timeline, 'loop')
    predictions = model.predict_proba(timeline_int)
    winratearr = [(1-percentage[0]) for percentage in predictions]
    return winratearr, timeline

logit_winrates_with_interactions, game_details_logitint=predict_with_int('Ancient Cistern LE (10).SC2Replay', pvt_logitint)

def predict_game_all(path):
    winr1, gamedet = predict_game(path, pvt_logit)
    winr2, gamedet2 = predict_with_int(path, pvt_logitint)
    fig= plt.plot(gamedet)
    fig= plt.plot(gamedet2)
    plt.xlabel('gameloop')
    plt.ylabel('winrate')
    plt.title('winrate by gameloop')
    plt.savefig('winrate by gameloop.png')
    plt.cla()