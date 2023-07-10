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
    replay_ls={'pvp':pd.DataFrame(),
                    'pvt':pd.DataFrame(),
                    'pvz':pd.DataFrame(),
                    'zvt':pd.DataFrame(),
                    'tvt':pd.DataFrame(),
                    'zvz':pd.DataFrame()}

    for obj_path in tqdm.tqdm(dir_list):
        if obj_path.is_file():
            try:
                replay = parse_replay(obj_path, local=True, tick=90)
                # do stuff with the data
            except:
                pass
        try:
            player1_workername=list(replay[1][2][1]['unit'].keys())[0]
            player2_workername=list(replay[1][2][2]['unit'].keys())[0]
            player_workertypes=[player1_workername, player2_workername]
            if 'SCV' in player_workertypes:
                if 'Probe' in player_workertypes:
                    #replay_ls['pvt'].append(replay)
                    matchup='pvt'
                elif 'Egg' in player_workertypes:
                    #replay_ls['zvt'].append(replay)
                    matchup='zvt'
                else:
                    #replay_ls['tvt'].append(replay)
                    matchup='tvt'
            elif 'Probe' in player_workertypes:
                if ('Egg' in player_workertypes)|('Larva') in player_workertypes:
                    #replay_ls['pvz'].append(replay)
                    matchup='pvz'
                else:
                    #replay_ls['pvp'].append(replay)
                    matchup='pvp'
            elif ('Egg' in player_workertypes)|('Larva') in player_workertypes:
                #replay_ls['zvz'].append(replay)
                matchup='zvz'
            timeline=pd.DataFrame(gen_total_timeline(replay, matchup))
            print(timeline)
            replay_ls[matchup]=replay_ls[matchup].append(timeline, ignore_index=True)
        except IndexError:
            pass
    return replay_ls

#define function to add prefix to player keys in mirrors (to prevent repeated keys)
def prepend_playernumbers(dictionary, prefix):
    updated_dict = {}
    for key, value in dictionary.items():
        new_key = prefix + str(key)
        updated_dict[new_key] = value
    return updated_dict

def generate_snapshot(snapshot, player_codes, result, matchup):
    #generate empty unit data
    snapshot_dict={}
    #check if mirror matchup
    mirror=matchup in ['pvp', 'tvt', 'zvz']
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
                {(race+'_gas_collection_rate'):player_info['resource_collection_rate']['gas']},
                {(race+'_unspent_minerals'):player_info['unspent_resources']['minerals']},
                {(race+'_unspent_gas'):player_info['unspent_resources']['gas']}]

        if not mirror:
            snapshot_dict.update(unitsdict)
            snapshot_dict.update(buildingdict)
            snapshot_dict.update(upgradedict)
            for stats in resource_stats:
                snapshot_dict.update(stats)

        elif mirror:
            player_dict={}
            player_dict.update(unitsdict)
            player_dict.update(buildingdict)
            player_dict.update(upgradedict)
            for stats in resource_stats:
                player_dict.update(stats)
            player='player_'+str(i+1)+'_'
            player_dict=prepend_playernumbers(player_dict, player)
            snapshot_dict.update(player_dict)

    snapshot_dict.update({'result':result}) 
    snapshot_dict.update({'loop':snapshot[1]['gameloop']})
    return snapshot_dict

race_codes={
    'SCV':'Terran',
    'Egg': 'Zerg',
    'Larva': 'Zerg',
    'Probe': 'Protoss'
}

def gen_total_timeline(game, matchup:str):
    player1_workername=list(game[1][2][1]['unit'].keys())[0]
    player2_workername=list(game[1][2][2]['unit'].keys())[0]
    player1_race=race_codes[player1_workername]
    player2_race=race_codes[player2_workername]
    #if pvt, result=1 if protoss win
    if matchup=='pvt':
        player1_isprotoss=player1_race=='Protoss'
        player_race_codes={
            2-player1_isprotoss:'Protoss',
            player1_isprotoss+1:'Terran'
        }
        result=player_race_codes[game[4]['winner']]=='Protoss'
    #if pvz, result=1 if protoss win
    elif matchup=='pvz':
        player1_isprotoss=player1_race=='Protoss'
        player_race_codes={
            2-player1_isprotoss:'Protoss',
            player1_isprotoss+1:'Zerg'
        }
        result=player_race_codes[game[4]['winner']]=='Protoss'
    #if zvt, result=1 if zerg win
    elif matchup=='zvt':
        player1_iszerg=player1_race=='Zerg'
        player_race_codes={
            2-player1_iszerg:'Zerg',
            player1_iszerg+1:'Terran'
        }
        result=player_race_codes[game[4]['winner']]=='Zerg'
    #for mirror matchups result=1 if winner==1
    elif matchup in ['pvp', 'zvz', 'tvt']:
        if matchup=='pvp':
            player_race_codes={
                1:'Protoss',
                2:'Protoss'
            }
            result=game[4]['winner']==1
        elif matchup=='tvt':
            player_race_codes={
                1:'Terran',
                2:'Terran'
            }
            result=game[4]['winner']==1
        elif matchup=='zvz':
            player_race_codes={
                1:'Zerg',
                2:'Zerg'
            }
            result=game[4]['winner']==1
    timeline=game[1]
    total_timeline = [generate_snapshot(timepoint, player_race_codes, result, matchup) for timepoint in timeline]
    return total_timeline