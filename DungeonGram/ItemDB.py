from os.path import join
from json import load

f = open(join('Assets', 'idb_items.json'))
item_data = load(f)
f.close()

idb_items = {}
for item_name in item_data:
    item_info = item_data[item_name]
    item_type = item_info['item_type']

    if item_type not in idb_items:
        idb_items[item_type] = []

    idb_items[item_type].append(item_info)

for item_type in idb_items:
    idb_items[item_type].sort(key=lambda info: info['tier'])