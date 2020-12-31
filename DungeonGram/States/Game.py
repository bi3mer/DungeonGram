from .State import State

from itertools import repeat
from json import load
from os.path import join

class Game(State):
    __slots__ = [
        'ready_to_transition', 'items', 'tiers', 'entities', 'max_y', 'max_x',
        'entities', 'tiles', 'positions', 'healths', 'behaviors', 'map',
        'player_index']

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

        self.player_index = 0
        self.entities = []
        self.tiles = []     # 0 
        self.positions = [] # 1
        self.healths = []   # 2
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
            self.map.append(line)

            for x, char in enumerate(line):
                if char == '-':
                    continue

                if char not in entities:
                    raise TypeError(f'{char} in map not in entities')

                entity_info = entities[char]

                position_index = len(self.positions)
                self.positions.append([x,y])

                tile_index = len(self.tiles)
                self.tiles.append(char)

                type_index = len(self.types)
                self.types.append(entities[char]['type'])

                if 'health' in entity_info:
                    health_index = len(self.healths)
                else:
                    health_index = -1

                if 'behavior' in entity_info:
                    # TODO
                    behavior_index = -1
                else:
                    behavior_index = -1

                self.entities.append((tile_index, position_index, health_index, behavior_index))
            
        f.close()

        self.max_y = len(self.map)
        self.max_x = len(self.map[0])

    def get_player_actions(self):
        x, y = self.positions[self.player_index]

        # check up, down, left, and right. While doing so check for entities in 
        # the cardinal directions. If another entity is spotted in the map, then
        # there should be possible interactions like attack or use. 
        #
        # Lastly, once there is an inventory, the player should have the option 
        # to use the items in their inventory. They should only be able to hold 
        # onto one weapon and one pickaxe

    def update(self):
        valid_player_input = False
        while not valid_player_input:
            key_press = input('')

        self.ready_to_transition = True

    def draw(self):
        for row in self.map:
            print(row.strip())
        
    def should_transition(self):
        return self.ready_to_transition

    def reset(self):
        for key in self.tiers:
            self.tiers[key] = 0

        self.entities.clear()