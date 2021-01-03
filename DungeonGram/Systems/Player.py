from os import stat
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

        for entity_id, entity in enumerate(state.entities):
            if state.tiles[entity[TILE_INDEX]] == 'S':
                continue

            e_x, e_y = state.positions[entity[POSITION_INDEX]]
            if (x + 1 == e_x and y == e_y) or (x - 1 == e_x and y == e_y) or \
               (x == e_x and y == e_y + 1) or (x == e_x and y == e_y - 1):
                
                valid_actions.append((ATTACK_ACTION, player_id, entity_id))

                tile_char = state.tiles[entity[TILE_INDEX]]
                if tile_char == 'T' or tile_char == 'D' or tile_char == 'K' or tile_char == 'L':
                    valid_actions.append((USE_ACTION, player_id, entity_id))

        return valid_actions

    def get_actions(self, state, player_id):
        possible_actions = self.get_player_actions(state, player_id)

        print()
        for i, action in enumerate(possible_actions, 1):
            action_type = action[0]
            if action_type == ATTACK_ACTION:
                print(f'{i}) Attack {state.tiles[state.entities[action[2]][TILE_INDEX]]}')
            elif action_type == USE_ACTION:
                print(f'{i}) Use {state.tiles[state.entities[action[2]][TILE_INDEX]]}')

        try:
            key_press = input('\nEnter command: ')

            if key_press == 'a':
                if self.__can_move(state, player_id, (-1, 0)):
                    return (MOVE_ACTION, player_id, -1, 0)
                else:
                    return (MESSAGE_ACTION, 'Move command not possible')
            elif key_press == 's':
                if self.__can_move(state, player_id, (0, 1)):
                    return (MOVE_ACTION, player_id, 0, 1)
                else:
                    return (MESSAGE_ACTION, 'Move command not possible')
            elif key_press == 'd':
                if self.__can_move(state, player_id, (1, 0)):
                    return (MOVE_ACTION, player_id, 1, 0)
                else:
                    return (MESSAGE_ACTION, 'Move command not possible')
            elif key_press == 'w':
                if self.__can_move(state, player_id, (0, -1)):
                    return (MOVE_ACTION, player_id, 0, -1)
                else:
                    return (MESSAGE_ACTION, 'Move command not possible')
            else:
                index = int(key_press) - 1
                if index < 0 or index >= len(possible_actions):
                    return (MESSAGE_ACTION, f'No valid action found for {index + 1}')
                else:
                    return possible_actions[index]
        except ValueError:
            return (MESSAGE_ACTION, f'Received invalid command')