from os.path import join
from .State import State
from ..config import *

from ..ComponentManager import *
from ..EntityDB import *
from ..Systems import *

class Game(State):
    __slots__ = [
        'ready_to_transition', 'entities', 'entities', 'player_id', 'systems',
        'player_system']

    def __init__(self):
        # set up order of operatios for systems
        self.player_system = Player()
        self.systems = [
            BasicEnemy(),
            Guardian()
        ]

    def on_enter(self):
        self.ready_to_transition = False

        self.player_id = 0
        self.entities = []
        
        # temporary map building. To be replaced with procedural generation
        f = open(join('Assets', 'Levels', '0.txt'))
        cm_map = []

        for y, line in enumerate(f.readlines()):
            line = line.strip()
            cm_map.append(list(line))

            for x, char in enumerate(line):
                if char == '-':
                    continue

                if char not in edb_entities:
                    raise TypeError(f'{char} in map not in entities')

                entity_info = edb_entities[char]
                entity_id = len(self.entities)

                if char == '@':
                    self.player_id = entity_id

                pos_id = cm_add_position(x, y)
                tile_id = cm_add_tile(char)
                type_id = cm_add_type(entity_info['type'])

                if 'stats' in entity_info:
                    stats_info = entity_info['stats']
                    stats_id = cm_add_stats(stats_info['health'], stats_info['damage'])
                else:
                    stats_id = -1

                if 'system' in entity_info:
                    system_id = cm_add_stats(entity_info['system'])
                else:
                    system_id = -1

                self.entities.append((system_id, tile_id, pos_id, stats_id, type_id))
            
        f.close()

        self.max_y = len(self.map) - 1
        self.max_x = len(self.map[0]) - 1

    def on_exit(self):
        self.max_x = 0
        self.max_y
        del self.entities
        cm_reset()

    def run_action(self, action):
        entity_id = action[1]
        entity = self.entities[entity_id]
        if action[0] == MOVE_ACTION:
            _, old_x, old_y = self.positions[entity[1]]

            new_x =  old_x + action[2]
            new_y = old_y + action[3]

            self.positions[entity[1]][1] = new_x
            self.positions[entity[1]][2] = new_y

            self.map[old_y][old_x] = '-'
            self.map[new_y][new_x] = self.tiles[entity[0]][1]
        else:
            raise TypeError(f'unhandled action type: {action[0]}')


    def update(self):
        a = self.player_system.get_action(self.entities[self.player_id])
        if a == None:
            return
        self.run_action(a)

        for system in self.systems:
            actions = []
            for entity in self.entities:
                a = system.get_action(entity)
                if a != None:
                    actions.append(a)

            for a in actions:
                self.run_action(a)

        if self.stats[self.entities[self.player_id][STAT_INDEX]][2] <= 0:
            self.should_transition = True

    def draw(self):
        for row in self.map:
            print(''.join(row))
        
    def should_transition(self):
        return self.ready_to_transition

    def reset(self):
        for key in self.tiers:
            self.tiers[key] = 0

        self.entities.clear()