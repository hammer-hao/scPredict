from pathlib import Path
import re
import sc2reader
from tqdm import tqdm
from zephyrus_sc2_parser import parse_replay as z_parse_replay

class Parser():
    def __init__(self, path):
        self.path = Path(path)
    
    def parse_replays(self):
        all_replays = []
        for file in tqdm(self.path.iterdir()):
            try:
                replay_path = str(file)
                all_replays.append(parse_replay(replay_path))
            except Exception as e:
                print(f"Error processing {file}: {e}")
        return all_replays
    
    def parse_replays_lite(self):
        all_replays = []
        for file in tqdm(self.path.iterdir()):
            try:
                replay_path = str(file)
                all_replays.append(parse_replay_lite(replay_path))
            except Exception as e:
                print(f"Error processing {file}: {e}")
        return all_replays

def parse_replay(path):
    replay = sc2reader.load_replay(path)
    winner = replay.winner
    stats = []
    for event in replay.events:
        if not hasattr(event, 'location'):
            event.location=(0,0)
            has_location = False
        else:
            has_location = True

        if event.name == "PlayerStatsEvent":
            stats.append(event)
    return stats, winner

def parse_replay_lite(path):
    replay = sc2reader.load_replay(path)
    winner = int(re.search(r"Team (\d+)", str(replay.winner)).group(1))
    stats = {}
    for event in replay.events:
        if event.name == "PlayerStatsEvent":
            player_id = event.pid
            minerals_rate = event.minerals_collection_rate
            gas_rate = event.vespene_collection_rate
            minerals_bank = event.minerals_current
            gas_bank = event.vespene_current
            army_lost_minerals = event.minerals_lost_army
            army_lost_gas = event.vespene_lost_army
            economy_lost_minerals = event.minerals_lost_economy
            economy_lost_gas = event.vespene_lost_economy
            tech_spent_minerals = event.minerals_lost_technology
            tech_spent_gas = event.vespene_lost_technology
            worker_count = event.workers_active_count
            army_in_progress_minerals = event.minerals_used_in_progress_army
            army_in_progress_gas = event.vespene_used_in_progress_army
            economy_in_progress = event.minerals_used_in_progress_economy
            upgrades_in_progress = event.vespene_used_in_progress_technology
            player_frame_data = {'minerals_rate': minerals_rate,
                                 'gas_rate': gas_rate,
                                 'minerals_bank': minerals_bank,
                                 'gas_bank': gas_bank,
                                 'army_lost_minerals': army_lost_minerals,
                                 'army_lost_gas': army_lost_gas,
                                 'economy_lost_minerals': economy_lost_minerals,
                                 'economy_lost_gas': economy_lost_gas,
                                 'tech_spent_minerals': tech_spent_minerals,
                                 'tech_spent_gas': tech_spent_gas,
                                 'worker_count': worker_count,
                                 'army_in_progress_minerals': army_in_progress_minerals,
                                 'army_in_progrss_gas': army_in_progress_gas,
                                 'economy_in_progress': economy_in_progress,
                                 'upgrades_in_progress': upgrades_in_progress}
            update = {player_id: player_frame_data}
            if event.second % 10 == 0:
                if event.second not in stats:
                    stats.update({event.second: update})
                else:
                    stats[event.second].update(update)
    return stats, winner

class SC2TimeFrame():
    def __init__(self):
        self.dict = {}
    
    def update(self, player, stat, value):
        self.dict[f'player{player}_{stat}'] = value

    def update_meta(self, stat, value):
        self.dict[stat] = value

class ZGameParser():
    def __init__(self, ticks=112):
        self.ticks = ticks
        self.generate_prefix = lambda player, content: f'player{player}_{content}'
        self.timeline = []

    def reset(self):
        self.timeline = []

    def parse(self, path):
        replay = z_parse_replay(path, local=True, tick=self.ticks, network=False)
        race_1 = replay.players[1].race
        race_2 = replay.players[2].race
        name_1 = replay.players[1].name
        name_2 = replay.players[2].name
        winner = replay.metadata['winner']
        invert_players = False
        if race_1 == "Protoss":
            if race_2 == "Protoss":
                matchup = "pvp"
            elif race_2 == "Terran":
                matchup = "pvt"
            elif race_2 == "Zerg":
                matchup = "pvz"
        if race_1 == "Terran":
            if race_2 == "Protoss":
                matchup = "pvt"
                invert_players = True
            elif race_2 == "Terran":
                matchup = "tvt"
            elif race_2 == "Zerg":
                matchup = "tvz"
        if race_1 == "Zerg":
            if race_2 == "Protoss":
                matchup = "pvz"
                invert_players = True
            elif race_2 == "Terran":
                matchup = "tvz"
                invert_players = True
            elif race_2 == "Zerg":
                matchup = "zvz"

        if invert_players:
            winner = 3 - int(winner)
            name_2 = replay.players[1].name
            name_1 = replay.players[2].name

        for frame in replay.timeline:
            timeframe = SC2TimeFrame()
            timeframe.update_meta('winner', winner)
            timeframe.update_meta('gameloop', frame[1]['gameloop'])
            for player, stats in frame.items():
                if invert_players:
                    player = 3 - int(player)
                timeframe.update(player, 'mineral_collection_rate', stats['resource_collection_rate']['minerals'])
                timeframe.update(player, 'gas_collection_rate', stats['resource_collection_rate']['gas'])
                timeframe.update(player, 'unspent_minerals', stats['unspent_resources']['minerals'])
                timeframe.update(player, 'unspent_gas', stats['unspent_resources']['gas'])
                timeframe.update(player, 'army_value_minerals', stats['army_value']['minerals'])
                timeframe.update(player, 'army_value_gas', stats['army_value']['gas'])
                timeframe.update(player, 'resources_lost_minerals', stats['resources_lost']['minerals'])
                timeframe.update(player, 'resources_lost_gas', stats['resources_lost']['gas'])
                timeframe.update(player, 'resources_collected_minerals', stats['resources_collected']['minerals'])
                timeframe.update(player, 'resources_collected_gas', stats['resources_collected']['gas'])
                for unit_name, unit_stats in stats['unit'].items():
                    timeframe.update(player, f'{unit_name}_alive', unit_stats['live'])
                    timeframe.update(player, f'{unit_name}_dead', unit_stats['died'])
                    timeframe.update(player, f'{unit_name}_prod', unit_stats['in_progress'])
                for building_name, building_stats in stats['building'].items():
                    timeframe.update(player, f'{building_name}_alive', building_stats['live'])
                    timeframe.update(player, f'{building_name}_dead', building_stats['died'])
                    timeframe.update(player, f'{building_name}_prod', building_stats['in_progress'])
                for upgrade in stats['upgrade']:
                    timeframe.update(player, upgrade, 1)

            self.timeline.append(timeframe.dict)
        
        # returns a list of dictonaries, each entry representing a tick in the game
        return self.timeline, matchup, name_1, name_2

class ZBulkParser():
    def __init__(self):
        self.parser = ZGameParser()
        self.path = None
        self.dict = {'pvp':[],
                     'pvt':[],
                     'pvz':[],
                     'tvz':[],
                     'tvt':[],
                     'zvz':[]}
    
    def parse_folder(self, path_to_folder):
        self.path = Path(path_to_folder)
        for file in tqdm(self.path.iterdir()):
            try:
                replay_path = str(file)
                timeline, matchup, name_1, name_2 = self.parser.parse(replay_path)
                self.dict[matchup] += timeline
                self.parser.reset()
            except Exception as e:
                print(f'Error processing {file}: {e}')
        
        return self.dict