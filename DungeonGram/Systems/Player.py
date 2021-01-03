from .System import System
from ..config import *

class Player(System):
    def __init__(self):
        super().__init__()

    def __can_move(self, state, player_id, direction):
        x, y = state.positions[state.entities[player_id][POSITION_INDEX]]
        new_x = x + direction[0]
        if new_x <= 0 or new_x >= state.max_x:
            return False

        new_y = y + direction[1]
        if new_y <= 0 or new_y >= state.max_y:
            return False

        return state.map[new_y][new_x] == '-'

    def get_player_actions(self, state, player_id):
        valid_actions = []
        x, y = state.positions[state.entities[player_id][POSITION_INDEX]]

        # Once there is an inventory, the player should have the option 
        # to use the items in their inventory. They should only be able to hold 
        # onto one weapon and one pickaxe

        return valid_actions

    def get_action(self, state, player_id):
        possible_actions = self.get_player_actions(state, player_id)

        print()
        for i, action in enumerate(possible_actions):
            continue
        
        try:
            key_press = input('\nEnter command: ')

            if key_press == 'a':
                if self.__can_move(state, player_id, (-1, 0)):
                    return (MOVE_ACTION, player_id, -1, 0)
            elif key_press == 's':
                if self.__can_move(state, player_id, (0, 1)):
                    return (MOVE_ACTION, player_id, 0, 1)
            elif key_press == 'd':
                if self.__can_move(state, player_id, (1, 0)):
                    return (MOVE_ACTION, player_id, 1, 0)
            elif key_press == 'w':
                if self.__can_move(state, player_id, (0, -1)):
                    return (MOVE_ACTION, player_id, 0, -1)
            else:
                index = int(key_press)
                if index < 0 or index >= len(possible_actions):
                    return
                else:
                    self.run_action(possible_actions[index])
        except ValueError:
            return