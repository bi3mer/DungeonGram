from os.path import join
from json import load
from random import sample

f = open(join('Assets', 'items.json'))
idb_items = load(f)
f.close()

# NOTE: this will be used if a tier unlock system is added.
# idb_items = {}
# for item_name in item_data:
#     item_info = item_data[item_name]
#     item_type = item_info['item_type']

#     if item_type not in idb_items:
#         idb_items[item_type] = []

#     idb_items[item_type].append(item_info)

# for item_type in idb_items:
#     idb_items[item_type].sort(key=lambda info: info['tier'])

def idb_get_random_item_name():
    return sample(list(idb_items.keys()), 1)[0]