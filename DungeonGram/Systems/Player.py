from .System import System
from ..config import *

from ..ComponentManager import *

class Player(System):
    def __init__(self):
        super().__init__()

    def get_player_actions(self, entity_id, pos_id):
        valid_actions = []

        x, y = cm_positions[pos_id]
        for modifier in DIRECTIONS:
            new_x = x + modifier[0]
            if new_x <= 0 or new_x >= self.max_x:
                continue

            new_y = y + modifier[1]
            if new_y <= 0 or new_y >= self.max_y:
                continue

            if self.map[new_y][new_x] == '-':
                valid_actions.append((MOVE_ACTION, entity_id, modifier[0], modifier[1]))

        # Once there is an inventory, the player should have the option 
        # to use the items in their inventory. They should only be able to hold 
        # onto one weapon and one pickaxe

        return valid_actions

    def get_action(self, entity, entity_id):
        _, _, pos_id, _, type_id = entity
        if type_id != 'player':
            return None
            
        possible_actions = self.get_player_actions(entity_id, pos_id)

        print()
        for i, action in enumerate(possible_actions):
            continue
        
        try:
            key_press = input('\nEnter command: ')
            index = int(key_press)
            if index < 0 or index >= len(possible_actions):
                return
            else:
                self.run_action(possible_actions[index])
        except ValueError:
            return