from DungeonGram.config import IS_ACTIVE_INDEX


class GameState:
    def __init__(self):
        self.entities = []
        self.positions = []
        self.tiles = [] 
        self.stats = []
        self.types = []
        self.is_active = [True, False]
        self.systems = []

        self.map = None
        self.max_x = 0
        self.max_y = 0
        self.player_won = 0 # -1 lost, 0 playing, 1 lost

    def __eq__(self, other):
        return self.positions, self.stats, self.is_active, self.player_won == \
               other.positions, other.__states, other.is_active, other.player_won

    def __hash__(self):
        return hash(self.positions) + hash(self.stats) + hash(self.is_active) + hash(self.player_won)

    def copy(self):
        new_state = GameState()
        new_state.entities = self.entities
        new_state.positions = self.positions.copy()
        new_state.tiles = self.tiles
        new_state.stats = self.stats.copy()
        new_state.types = self.types
        new_state.is_active = self.is_active.copy()
        new_state.systems = self.systems

        new_state.map = self.map
        new_state.max_x = self.max_x
        new_state.max_y = self.max_y
        new_state.player_won = self.player_won

        return new_state

    ### Component Management 
    def __add_unique(self, component_array, value):
        for i, key in enumerate(component_array):
            if value == key:
                return i

        id = len(component_array)
        component_array.append(value)
        return id

    def __add_non_unique(self, component_array, value):
        id = len(component_array)
        component_array.append(value)
        return id

    def add_position(self, x, y):
        return self.__add_non_unique(self.positions, [x, y])

    def add_tile(self, tile):
        return self.__add_unique(self.tiles, tile)

    def add_stats(self, health, damage):
        return self.__add_non_unique(self.stats, [health, damage])

    def add_type(self, type):
        return self.__add_unique(self.types, type)

    def add_is_active(self, is_active):
        return self.__add_unique(self.is_active, is_active)

    def add_entity(self, entity):
        return self.__add_non_unique(self.entities, entity)

    def add_system(self, system_name):
        return self.__add_unique(self.systems, system_name)

    def change_entity_is_active(self, entity_id, is_active):
        if is_active:
            self.entities[entity_id][IS_ACTIVE_INDEX] = 0
        else:
            self.entities[entity_id][IS_ACTIVE_INDEX] = 1

    def reset(self):
        self.positions.clear()
        self.entities.clear()
        self.stats.clear()
        
