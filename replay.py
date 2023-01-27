from zephyrus_sc2_parser import parse_replay
import configurations
import pandas as pd
from pathlib import Path
from zephyrus_sc2_parser import parse_replay
import tqdm

# change this to match the directory you're using
replays = Path('C:/Users/hammerhao/OneDrive/Documents/StarCraft II/Accounts/818931843/2-S2-1-10228956/Replays/Multiplayer')

def recursereplays(dir_path):
    """
    Recursively searches directories to parse replay files
    """
    dir_list=list(dir_path.iterdir())
    print(dir_list)
    replay_list=[]
    for obj_path in tqdm.tqdm(dir_list):
        if obj_path.is_file():
            try:
                replay = parse_replay(obj_path)
                replay_list.append(replay)
                # do stuff with the data
            except:
                pass
    return replay_list

replay_list = recursereplays(replays)

def generate_unit_snapshot(snapshot, player_codes, protosswin):
    #generate empty unit data
    totalunits={}
    for i in range(2):
        unitsdict={}
        for unitname in configurations.Units[player_codes[i+1]]:
            live=unitname+'_live'
            died=unitname+'_dead'
            inprogress=unitname+'_in_progress'
            thisunit=[{live:0}, {died:0}, {inprogress:0}]
            for dic in thisunit:
                unitsdict.update(dic)
        #find matching unit
        unitdetails=snapshot[i+1]['unit']
        for thisunitname, details in unitdetails.items():
            live=thisunitname+'_live'
            died=thisunitname+'_dead'
            inprogress=thisunitname+'_in_progress'
            ingameunitstats=[{live:details['live']}, {died:details['died']}, {inprogress:details['in_progress']}]
            for dic in ingameunitstats:
                unitsdict.update(dic)
        totalunits.update(unitsdict)
        totalunits.update({'Protosswin':protosswin})
        totalunits.update
    return totalunits

def gen_total_timeline(game):
    metadata=game[3]
    if 'creep' in metadata['race'][1]:
        player_codes={
            1:'Zerg',
            2:'Protoss'
        }
    elif 'creep' in metadata['race'][2]:
        player_codes={
            1:'Protoss',
            2:'Zerg'
        }
    protosswin=player_codes[game[4]['winner']]=='Protoss'
    timeline=game[1]
    total_timeline = [generate_unit_snapshot(timepoint, player_codes, protosswin) for timepoint in timeline]
    return total_timeline

pvz_replay_list=[]
for replay in replay_list:
    if ('creep' in replay[3]['race'][1]) | ('creep' in replay[3]['race'][2]):
        pvz_replay_list.append(replay)

totalunits=[]
for replay in tqdm.tqdm(pvz_replay_list):
    totalunits+=gen_total_timeline(replay)

df = pd.DataFrame(totalunits)
df.to_csv('pvzgames.csv')
'''
class replay:
    def __init__(self, link_to_replay):
        self.link=link_to_replay
    def parse_contents(self, tickinterval):
        self.timeline=parse_replay(self.link, tick=tickinterval)[1]
        for snapshot in self.timeline:
            generate_snapshot(snapshot, Protoss_index)
'''