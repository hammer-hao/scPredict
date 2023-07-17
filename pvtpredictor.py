from tkinter import *
from tkinter import filedialog
from pickle import load as pickleload
from zephyrus_sc2_parser import parse_replay
from training_features import pvt as pvtfeatures
from replay import gen_total_timeline
from pandas import DataFrame, concat
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

file = open(resource_path('pvt_test_logit_w_interactions.model'),'rb')
pvt_logitint=pickleload(file)
file.close()

df_dict={}
for feature in pvtfeatures:
    df_dict.update({feature:0})

def make_interactions(df, root):
    feature = root
    specific_feature = df[root]
    interaction_terms = DataFrame()
    for column in df.columns:
        if column != feature:
            interaction_term = specific_feature * df[column]  # Create the interaction term
            interaction_terms[column+'_interaction'] = interaction_term# Reshape and append to the list
    X_interactions = concat([df, interaction_terms], axis=1)
    return X_interactions

def predict_with_int(game, model):
    thisreplay=parse_replay(game, local=True, tick=90)
    totallist=[df_dict]+gen_total_timeline(thisreplay, 'pvt')
    timeline=DataFrame(totallist).drop(['result'], axis=1).fillna(0)
    timeline_int=make_interactions(timeline, 'loop')
    predictions = model.predict_proba(timeline_int)
    winratearr = [(1-percentage[0]) for percentage in predictions]
    return winratearr, timeline

def plot(data):
    ax.clear()
    ax.plot(data)
    ax.set_xlabel('gameloop')
    ax.set_ylabel('winrate')
    ax.set_title('winrate by gameloop')

window = Tk()
fig, ax = plt.subplots()

def openfile():
    global canvas
    path = filedialog.askopenfilename()
    logit_winrates_with_interactions, game_details_logitint=predict_with_int(path, pvt_logitint)
    top = Toplevel()
    top.title('Win rate progression')
    label = Label(text='win rates progression', master=top)
    label.config(font=('Courier', 32))
    label.pack()
    canvas = FigureCanvasTkAgg(fig, master=top)
    winrateplot=plot(logit_winrates_with_interactions)
    canvas.draw()
    canvas.get_tk_widget().pack()

    return path

button = Button(text='Select PVT replay', command=openfile)
button.pack()

window.mainloop()