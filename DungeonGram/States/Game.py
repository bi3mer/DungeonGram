from .State import State
from ..config import *

from itertools import repeat
from json import load
from os.path import join
from time import sleep

class Game(State):
    __slots__ = [
        'ready_to_transition', 'items', 'tiers', 'entities', 'max_y', 'max_x',
        'entities', 'tiles', 'positions', 'healths', 'behaviors', 'map',
        'player_id', 'DIRECTIONS']

    def __init__(self):
        self.ready_to_transition = False

        # build items
        f = open(join('Assets', 'items.json'))
        item_data = load(f)
        f.close()

        self.items = {}
        self.tiers = {}
        for item_name in item_data:
            item_info = item_data[item_name]
            item_type = item_info['item_type']

            if item_type not in self.tiers:
                self.tiers[item_type] = 0
                self.items[item_type] = []

            self.items[item_type].append(item_info)

        for item_type in self.items:
            self.items[item_type].sort(key=lambda info: info['tier'])

        self.player_id = 0
        self.entities = []
        self.tiles = []     # 0 
        self.positions = [] # 1
        self.stats = []     # 2
        self.behaviors = [] # 3
        self.types = []     # 4

        # get entity types
        f = open(join('Assets', 'entities.json'))
        entities = load(f)
        f.close()
        
        # temporary map building. To be replaced with procedural generation
        f = open(join('Assets', 'Levels', '0.txt'))
        self.map = []

        for y, line in enumerate(f.readlines()):
            line = line.strip()
            self.map.append(list(line))

            for x, char in enumerate(line):
                if char == '-':
                    continue

                if char not in entities:
                    raise TypeError(f'{char} in map not in entities')

                entity_info = entities[char]
                entity_id = len(self.entities)

                if char == '@':
                    self.player_id = entity_id

                position_index = len(self.positions)
                self.positions.append([entity_id, x, y])

                tile_index = len(self.tiles)
                self.tiles.append((entity_id, char))

                type_index = len(self.types)
                self.types.append((entity_id, entities[char]['type']))

                if 'stats' in entity_info:
                    stats_index = len(self.stats)
                    stats_info = entity_info['stats']
                    print(stats_info)
                    self.stats.append([entity_id, stats_info['health'], stats_info['damage']])
                else:
                    stats_index = -1

                if 'behavior' in entity_info:
                    # TODO
                    behavior_index = -1
                else:
                    behavior_index = -1

                self.entities.append((tile_index, position_index, stats_index, behavior_index, type_index))
            
        f.close()

        self.max_y = len(self.map) - 1
        self.max_x = len(self.map[0]) - 1

    def get_player_actions(self):
        valid_actions = []

        _, x, y = self.positions[self.player_id]
        for modifier in DIRECTIONS:
            new_x = x + modifier[0]
            if new_x <= 0 or new_x >= self.max_x:
                continue

            new_y = y + modifier[1]
            if new_y <= 0 or new_y >= self.max_y:
                continue

            if self.map[new_y][new_x] == '-':
                valid_actions.append((MOVE_ACTION, self.player_id, new_x, new_y))

        # Once there is an inventory, the player should have the option 
        # to use the items in their inventory. They should only be able to hold 
        # onto one weapon and one pickaxe

        return valid_actions

    def run_action(self, action):
        entity_id = action[1]
        entity = self.entities[entity_id]
        if action[0] == MOVE_ACTION:
            _, old_x, old_y = self.positions[entity[1]]
            self.positions[entity[1]][1] = action[2]
            self.positions[entity[1]][2] = action[3]

            self.map[old_y][old_x] = '-'
            self.map[action[3]][action[2]] = self.tiles[entity[0]][1]
        else:
            raise TypeError(f'unhandled action type: {action[0]}')

    def update(self):
        possible_actions = self.get_player_actions()

        print()
        for i, action in enumerate(possible_actions):
            if action[0] == MOVE_ACTION:
                action[0]
                print(f'{i}) move')
        try:
            key_press = input('\nEnter command: ')
            index = int(key_press)
            if index < 0 or index >= len(possible_actions):
                print('Please enter a numberr associated with the commands above.')
                sleep(0.3)
                return
            else:
                self.run_action(possible_actions[index])
        except ValueError:
            print('\nPlease only enter the index associated with the command.')
            sleep(0.3)
            return

        # if the input is valid, then we can let the entities do their thing, else
        # we can't.

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