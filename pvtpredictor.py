from tkinter import *
from tkinter import filedialog
from pickle import load as pickleload
from zephyrus_sc2_parser import parse_replay
import training_features
from replay import gen_total_timeline
from pandas import DataFrame, concat
from sklearn import linear_model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import os

#resource path for packaging
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#model dictionary
model_dict={}
for matchup in ['pvt', 'pvz', 'zvt', 'tvt', 'zvz', 'pvp']:
    model_path='models/'+matchup+'_logit_temporal.model'
    file = open(resource_path(model_path),'rb')
    thismodel=pickleload(file)
    model_dict.update({matchup:thismodel})
    file.close()

features_dict={
    'pvp':training_features.pvp,
    'pvz':training_features.pvz,
    'pvt':training_features.pvt,
    'zvt':training_features.zvt,
    'tvt':training_features.tvt,
    'zvz':training_features.zvz
}

#get matchup from replay
def get_matchup(gamepath):
    replay=parse_replay(gamepath, local=True, tick=90)
    try:
        player1_workername=list(replay[1][2][1]['unit'].keys())[0]
        player2_workername=list(replay[1][2][2]['unit'].keys())[0]
        player_workertypes=[player1_workername, player2_workername]
        if 'SCV' in player_workertypes:
                    if 'Probe' in player_workertypes:
                        matchup='pvt'
                    elif ('Egg' in player_workertypes)|(('Larva') in player_workertypes):
                        matchup='zvt'
                    elif ('Probe' not in player_workertypes) & ('Egg' not in player_workertypes) & ('Larva' not in player_workertypes):
                        matchup='tvt'
        elif 'Probe' in player_workertypes:
                    if ('Egg' in player_workertypes)|(('Larva') in player_workertypes):
                        matchup='pvz'
                    elif ('Egg' not in player_workertypes)&(('Larva') not in player_workertypes):
                        matchup='pvp'
        elif ('Egg' in player_workertypes)|(('Larva') in player_workertypes):
                    matchup='zvz'
    except IndexError:
        matchup='None'
    del replay
    return matchup

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

def predict_with_int(game, model, matchup):
    df_dict={}
    features_total=features_dict[matchup]
    for feature in features_total:
        df_dict.update({feature:0})
    print(df_dict)
    thisreplay=parse_replay(game, local=True, tick=90)
    totallist=[df_dict]+gen_total_timeline(thisreplay, matchup)
    timeline=DataFrame(totallist).drop(['result'], axis=1).fillna(0)
    columns_bool=timeline.columns.isin(features_total)
    filtered_timeline=timeline.loc[:,columns_bool]
    timeline_int=make_interactions(filtered_timeline, 'loop')
    index=list(model[1])
    timeline_int=timeline_int[index]
    predictions = model[0].predict_proba(timeline_int)
    winratearr = [(1-percentage[0]) for percentage in predictions]
    return winratearr, timeline

def plot(data):
    global axvline
    ax.clear()
    ax.plot(data)
    ax.set_xlabel('gameloop')
    ax.set_ylabel('winrate')
    ax.set_title('winrate by gameloop')
    axvline=ax.axvline(x=currentloop, linestyle='dashed')

window = Tk()
window.minsize(300,100)
window.maxsize(300,100)
fig, ax = plt.subplots()

currentloop=0

def go_forward():
    global currentloop
    global canvas
    global axvline
    global details
    global details_label
    currentloop+=1
    axvline.set_data([currentloop, currentloop], [0,1])
    canvas.draw()
    canvas.get_tk_widget().pack()
    details_label='current gameloop: '+str(currentloop)+'   gametime: '+str((currentloop*5)//60)+':'+str((currentloop*5)%60)+'   winrate: '+str(logit_winrates_with_interactions[currentloop])
    details['text']=details_label
    

def go_backward():
    global currentloop
    global canvas
    global axvline
    global details
    global details_label
    currentloop-=1
    axvline.set_data([currentloop, currentloop], [0,1])
    canvas.draw()
    canvas.get_tk_widget().pack()
    details_label='current gameloop: '+str(currentloop)+'   gametime: '+str((currentloop*5)//60)+':'+str((currentloop*5)%60)+'   winrate: '+str(logit_winrates_with_interactions[currentloop])
    details['text']=details_label

def go_forward_timesfive():
    global currentloop
    global canvas
    global axvline
    global details
    global details_label
    currentloop+=5
    axvline.set_data([currentloop, currentloop], [0,1])
    canvas.draw()
    canvas.get_tk_widget().pack()
    details_label='current gameloop: '+str(currentloop)+'   gametime: '+str((currentloop*5)//60)+':'+str((currentloop*5)%60)+'   winrate: '+str(logit_winrates_with_interactions[currentloop])
    details['text']=details_label
    

def go_backward_timesfive():
    global currentloop
    global canvas
    global axvline
    global details
    global details_label
    currentloop-=5
    axvline.set_data([currentloop, currentloop], [0,1])
    canvas.draw()
    canvas.get_tk_widget().pack()
    details_label=('current gameloop: '+str(currentloop)+
    '   gametime: '+str((currentloop*5)//60)+':'+str((currentloop*5)%60)+
    '   winrate: '+str(logit_winrates_with_interactions[currentloop]))
    details['text']=details_label

def go_to_start():
    global currentloop
    global canvas
    global axvline
    global details
    global details_label
    currentloop=0
    axvline.set_data([currentloop, currentloop], [0,1])
    canvas.draw()
    canvas.get_tk_widget().pack()
    details_label=('current gameloop: '+str(currentloop)+
    '   gametime: '+str((currentloop*5)//60)+':'+str((currentloop*5)%60)+
    '   winrate: '+str(logit_winrates_with_interactions[currentloop]))
    details['text']=details_label

def go_to_end():
    global currentloop
    global canvas
    global axvline
    global gamelength
    global details
    global details_label
    currentloop=gamelength
    axvline.set_data([currentloop, currentloop], [0,1])
    canvas.draw()
    canvas.get_tk_widget().pack()
    details_label=('current gameloop: '+str(currentloop)+
    '   gametime: '+str((currentloop*5)//60)+':'+str((currentloop*5)%60)+
    '   winrate: '+str(logit_winrates_with_interactions[currentloop]))
    details['text']=details_label

def openfile():
    global canvas
    global currentloop
    global gamelength
    global logit_winrates_with_interactions
    global details
    global details_label
    path = filedialog.askopenfilename()
    matchup=get_matchup(path)
    model=model_dict[matchup]
    logit_winrates_with_interactions, game_details=predict_with_int(path, model, matchup=matchup)
    gamelength=len(logit_winrates_with_interactions)
    top = Toplevel()

    top.minsize(640,640)
    top.maxsize(640,640)
    top.title('Win rate progression')
    label = Label(text='win rates progression', master=top)
    label.config(font=('Courier', 32))
    label.pack()

    canvas = FigureCanvasTkAgg(fig, master=top)
    winrateplot=plot(logit_winrates_with_interactions)
    currentloop=0
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    controls=Frame(master=top)
    controls.pack()
    front=Button(text='Start', command=go_to_start, master=controls)
    forward_timesfive=Button(text='>>', command=go_forward_timesfive, master=controls)
    forward=Button(text='>', command=go_forward, master=controls)
    backward=Button(text='<', command=go_backward, master=controls)
    backward_timesfive=Button(text='<<', command=go_backward_timesfive, master=controls)
    end=Button(text='End', command=go_to_end, master=controls)
    front.pack(side=LEFT)
    backward_timesfive.pack(side=LEFT)
    backward.pack(side=LEFT)
    forward.pack(side=LEFT)
    forward_timesfive.pack(side=LEFT)
    end.pack(side=LEFT)
    details_label=('current gameloop: '+str(currentloop)+
    '   gametime: '+str((currentloop*5)//60)+':'+str((currentloop*5)%60)+
    '   winrate: '+str(logit_winrates_with_interactions[currentloop]))
    details=Label(master=top, text=details_label)
    details.pack(side=BOTTOM)

    return path

button = Button(text='Select any 1v1 replay', command=openfile)
button.pack()

window.mainloop()