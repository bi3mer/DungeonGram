from os.path import join
from random import sample

from .GameState import GameState
from .State import State
from ..EntityDB import *
from ..Systems import *
from ..config import *
from ..ItemDB import *

class Game(State):
    def __init__(self):
        self.player_system = Player()
        self.systems = [
            BasicEnemy(),
            Guardian()
        ]

        self.state = GameState()
        self.messages = []

    def on_enter(self):
        self.ready_to_transition = False

        self.player_id = 0
        
        # temporary map building from level file. This will be replaced with 
        # procedural generation
        f = open(join('Assets', 'Levels', '000.txt'))
        self.state.map = []

        for y, line in enumerate(f.readlines()):
            line = line.strip()
            self.state.map.append(list(line))

            for x, char in enumerate(line):
                if char == '-':
                    continue

                if char not in edb_entities:
                    raise TypeError(f'{char} in map not in entities')

                entity_info = edb_entities[char]
                pos_id = self.state.add_position(x, y)
                tile_id = self.state.add_tile(char)

                if 'type' in entity_info:
                    type_id = self.state.add_type(entity_info['type'])
                else:
                    type_id = -1

                if 'is_active' in entity_info:
                    is_active_id = self.state.add_is_active(entity_info['is_active'])
                else:
                    is_active_id = self.state.add_is_active(False)
                    
                if 'stats' in entity_info:
                    stats_info = entity_info['stats']
                    stats_id = self.state.add_stats(stats_info['health'], stats_info['damage'])
                else:
                    stats_id = -1

                if 'system' in entity_info:
                    system_id = self.state.add_system(entity_info['system'])
                else:
                    system_id = -1

                entity_id = self.state.add_entity([system_id, tile_id, pos_id, stats_id, type_id, is_active_id])
                if char == '@':
                    self.player_id = entity_id
            
        f.close()

        self.state.max_y = len(self.state.map)
        self.state.max_x = len(self.state.map[0])

    def on_exit(self):
        self.state.reset()

    def run_action(self, action):
        action_type = action[0]
        if action_type == MOVE_ACTION:
            entity_id = action[1]
            entity = self.state.entities[entity_id]
            
            old_x, old_y = self.state.positions[entity[POSITION_INDEX]]
            new_x = old_x + action[2]
            new_y = old_y + action[3]

            self.state.positions[entity[POSITION_INDEX]][0] = new_x
            self.state.positions[entity[POSITION_INDEX]][1] = new_y

            self.state.map[old_y][old_x] = '-'
            self.state.map[new_y][new_x] = self.state.tiles[entity[TILE_INDEX]]
        elif action_type == MESSAGE_ACTION:
            self.messages.append(action[1])
        elif action_type == USE_ACTION:
            target_entity = self.state.entities[action[2]]
            target_char = self.state.tiles[target_entity[TILE_INDEX]]

            if target_char == 'T':
                item_name = idb_get_random_item_name()
                # self.messages.append(f'Picked up {item_name}.')
                self.messages.append(f'Picked up {item_name} but not added to inventory.')
            elif target_char == 'D':
                self.messages.append('You open the door...')
            elif target_char == 'L':
                self.messages.append('Locked doors not implemented')
            elif target_char == 'K':
                self.messages.append('Picked up a key. use it to open locked doors (L). Not added to inventory yet.')
            else:
                raise TypeError(f'Unhandled use type: {target_char}')
            
            # remove the entity
            x, y = self.state.positions[target_entity[POSITION_INDEX]]
            self.state.map[y][x] = '-'
            self.state.entities[action[2]][POSITION_INDEX] = -1
            

        elif action_type == ATTACK_ACTION:
            pass
        else:
            raise TypeError(f'unhandled action type: {action[0]}')

    def update(self):
        a = self.player_system.get_actions(self.state, self.player_id)
        if a == None:
            return
        self.run_action(a)

        for system in self.systems:
            actions = system.get_actions(self.state, self.player_id)
            for a in actions:
                if a != None:
                    self.run_action(a)

        if self.state.stats[self.state.entities[self.player_id][STAT_INDEX]][0] <= 0:
            self.should_transition = True

    def draw(self):
        for message in self.messages:
            print(message)

        self.messages.clear()
        print()

        for row in self.state.map:
            print(''.join(row))

    def should_transition(self):
        return self.ready_to_transition

    def reset(self):
        self.state.clear()