from pathlib import Path
import torch
import sc2reader
from tqdm import tqdm

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