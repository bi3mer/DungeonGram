cm_positions = []
cm_tiles = [] 
cm_stats = []
cm_types = []
cm_systems = []

cm_map = None
cm_max_x = 0
cm_max_y = 0

def __add_unique(component_array, value):
    for i, key in enumerate(component_array):
        if value == key:
            return i

    id = len(component_array)
    component_array.append(value)
    return id

def __add_non_unique(component_array, value):
    id = len(component_array)
    component_array.append(value)
    return id

def cm_add_position(x, y):
    return __add_non_unique(cm_positions, [x, y])

def cm_add_tile(t):
    return __add_unique(cm_tiles, t)

def cm_add_stats(health, damage):
    return __add_non_unique(cm_stats, [health, damage])

def cm_add_type(t):
    return __add_unique(cm_types, t)

def cm_add_system(sys_name):
    return __add_unique(cm_systems, sys_name)

def cm_reset():
    cm_positions.clear()
    cm_stats.clear()
    