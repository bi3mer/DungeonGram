from .State import State

from itertools import repeat
from json import load
from os.path import join

class Game(State):
    __slots__ = [
        'ready_to_transition', 'items', 'tiers', 'entities', 'max_y', 'max_x',
        'entities', 'tiles', 'positions', 'healths', 'behaviors']

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

        self.max_y = 14
        self.max_x = 30

        self.entities = []
        self.tiles = []     # 0 
        self.positions = [] # 1
        self.healths = []   # 2
        self.behaviors = [] # 3

    def update(self):
        input()
        self.ready_to_transition = True

    def draw(self):
        mat = [[None for _, i in repeat(None, self.max_x)] for __, ii in repeat(None, self.max_y)]
        for entity in self.entities:
            x, y = self.positions[entity[1]]
            mat[y][x] = self.tiles[entity[0]]
        
    def should_transition(self):
        return self.ready_to_transition

    def reset(self):
        for key in self.tiers:
            self.tiers[key] = 0

        self.entities.clear()