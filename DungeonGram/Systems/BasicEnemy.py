from DungeonGram.config import *
from DungeonGram.Utility.Distance import manhattan

'''
TODO:
- some kind of line of sight to see if the enemy can actually see the player
  would be a nice addition. In 000.txt, the enemies can activate even if they
  are behind walls which isn't exactly ideal.
'''

class BasicEnemy:
    def get_actions(self, state, player_id):
        actions = []
        
        p_x, p_y = state.positions[state.entities[player_id][POSITION_INDEX]]
        for entity_id, entity in enumerate(state.entities):
            if entity[TYPE_INDEX] == -1:
                continue

            e_type = state.types[entity[TYPE_INDEX]]
            if e_type != 'being':
                continue

            e_x, e_y = state.positions[entity[POSITION_INDEX]]
            if not state.is_active[entity[IS_ACTIVE_INDEX]]:
                if manhattan(p_x, p_y, e_x, e_y) <= SKELETON_ACTIVATE_DIST:
                    tile_char = state.tiles[entity[TILE_INDEX]]
                    actions.append((MESSAGE_ACTION, f'{tile_char} has awakened!'))
                    state.change_entity_is_active(entity_id, True)

                continue
            
            # otherwise passfind stupidly
            s_x, s_y = state.positions[entity[POSITION_INDEX]]
            dist = 10000
            best_modifier = None

            for modifier in DIRECTIONS:
                new_x = s_x + modifier[0]
                new_y = s_y + modifier[1]

                if new_x == p_x and new_y == p_y:
                    actions.append((ATTACK_ACTION, entity_id, player_id))
                    break

                if new_x < 0 or new_x >= state.max_x:
                    continue

                if new_y < 0 or new_y >= state.max_y:
                    continue

                if state.map[new_y][new_x] == '-':
                    distance = manhattan(p_x, p_y, new_x, new_y)
                    if distance < dist:
                        dist = distance
                        best_modifier = modifier

            if best_modifier != None:
                actions.append((MOVE_ACTION, entity_id, best_modifier[0], best_modifier[1]))

        return actions