from zephyrus_sc2_parser import parse_replay
import configurations
import pandas as pd
from pathlib import Path
import tqdm

# change this to match the directory you're using
def recursereplays(dir_path):
    """
    Recursively searches directories to parse replay files
    """
    dir_list=list(dir_path.iterdir())
    print(dir_list)
    replay_list={'pvp':[],
                 'pvt':[],
                 'pvz':[],
                 'zvt':[],
                 'tvt':[],
                 'zvz':[]}
    for obj_path in tqdm.tqdm(dir_list):
        if obj_path.is_file():
            try:
                replay = parse_replay(obj_path, local=True)
                # do stuff with the data
            except:
                pass
        try:
            player1_workername=list(replay[1][2][1]['unit'].keys())[0]
            player2_workername=list(replay[1][2][2]['unit'].keys())[0]
        except IndexError:
            pass
        player_workertypes=[player1_workername, player2_workername]
        if 'SCV' in player_workertypes:
            if 'Probe' in player_workertypes:
                replay_list['pvt'].append(replay)
            if 'Drone' in player_workertypes:
                replay_list['zvt'].append(replay)
            else:
                replay_list['tvt'].append(replay)
        elif 'Probe' in player_workertypes:
            if 'Drone' in player_workertypes:
                replay_list['pvz'].append(replay)
            else:
                replay_list['pvp'].append(replay)
        elif 'Drone' in player_workertypes:
            replay_list['zvz'].append(replay)
    return replay_list

def generate_snapshot(snapshot, player_codes, protosswin):
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

        #getting updates data
        upgradedict={}
        for upgrade in player_info['upgrade']:
            thisupgrade={upgrade:1}
            upgradedict.update(thisupgrade)

        #getting resource data
        resource_stats=[{(race+'_mineral_collection_rate'):player_info['resource_collection_rate']['minerals']},
                {(race+'_gas_collection_rate'):player_info['resource_collection_rate']['minerals']},
                {(race+'_unspent_minerals'):player_info['unspent_resources']['minerals']},
                {(race+'_unspent_gas'):player_info['unspent_resources']['gas']}]

        snapshot_dict.update(unitsdict)
        snapshot_dict.update(buildingdict)
        snapshot_dict.update(upgradedict)
        snapshot_dict.update({'Protosswin':protosswin})
        for stats in resource_stats:
            snapshot_dict.update(stats)
    snapshot_dict.update({'loop':snapshot[1]['gameloop']})
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
    total_timeline = [generate_snapshot(timepoint, player_codes, protosswin) for timepoint in timeline]
    return total_timeline