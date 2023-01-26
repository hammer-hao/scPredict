from zephyrus_sc2_parser import parse_replay
import configurations
import pandas as pd

'''
class unit:
    def __init__(self, name, live, died, in_progress):
        self.name=name
        self.live=live
        self.died=died
        self.in_progress=in_progress
    def append(self):
        return [self.name, self.live, self.died, self.in_progress]
'''
game=parse_replay('test.SC2Replay', tick=100)

def generate_snapshot(thisgame):
    timeline=thisgame[1]
    metadata=thisgame[3]
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
    units_snapshot=timeline[100]
    #generate empty unit data
    totalunits={}
    for i in range(2):
        unitsdict={}
        for unitname in configurations.Units[player_codes[i+1]]:
            thisunit={unitname:[0, 0, 0]}
            unitsdict.update(thisunit)

        #find matching unit
        unitdetails=units_snapshot[i+1]['unit']
        for thisunitname, details in unitdetails.items():
            ingameunitstats={thisunitname:[details['live'], details['died'], details['in_progress']]}
            unitsdict.update(ingameunitstats)
        totalunits.update(unitsdict)
    return totalunits

print(generate_snapshot(game))

'''
class replay:
    def __init__(self, link_to_replay):
        self.link=link_to_replay
    def parse_contents(self, tickinterval):
        self.timeline=parse_replay(self.link, tick=tickinterval)[1]
        for snapshot in self.timeline:
            generate_snapshot(snapshot, Protoss_index)
'''