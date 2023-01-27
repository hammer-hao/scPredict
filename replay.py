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
    snapshot_dict={}
    for i in range(2):
        race=player_codes[i+1]
        player_info=snapshot[i+1]
        #getting units data
        unitsdict={}
        unitdetails=player_info['unit']
        for thisunitname, details in unitdetails.items():
            live=thisunitname+'_live'
            died=thisunitname+'_dead'
            inprogress=thisunitname+'_in_progress'
            ingameunitstats=[{live:details['live']}, {died:details['died']}, {inprogress:details['in_progress']}]
            for dic in ingameunitstats:
                unitsdict.update(dic)
        
        #getting buildings data
        buildingdict={}
        buildingdetails=player_info['building']
        for thisbuildingname, details in buildingdetails.items():
            live=thisbuildingname+'_live'
            died=thisbuildingname+'_dead'
            inprogress=thisbuildingname+'_in_progress'
            ingameunitstats=[{live:details['live']}, {died:details['died']}, {inprogress:details['in_progress']}]
            for dic in ingameunitstats:
                buildingdict.update(dic)

        #getting resource data
        resource_stats=[{(race+'_mineral_collection_rate'):player_info['resource_collection_rate']['minerals']},
                {(race+'_gas_collection_rate'):player_info['resource_collection_rate']['minerals']},
                {(race+'_unspent_minerals'):player_info['unspent_resources']['minerals']},
                {(race+'_unspent_gas'):player_info['unspent_resources']['gas']}]
        
        snapshot_dict.update(unitsdict)
        snapshot_dict.update(buildingdict)
        snapshot_dict.update({'Protosswin':protosswin})
        for stats in resource_stats:
            snapshot_dict.update(stats)
    return snapshot_dict

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