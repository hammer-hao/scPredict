import torch
import sc2reader

replay = sc2reader.load_replay('test.SC2Replay')

for event in replay.events:
    if not hasattr(event, 'location'):
        event.location=(0,0)
    print(f'{event.name} at {event.location} by {event.upkeep_pid}: {event.frame}')

class Parser():
    def __init__(self, path):
        self.path = path
    
    def parse_replays(self):
        sc2reader.load_replay('test.SC2Replay')

def parse_replay(path):
    replay = sc2reader.load_replay(path)
    for event in replay.events:
        if not hasattr(event, 'location'):
            event.location=(0,0)
            has_location = False
        else:
            has_location = True

        
        