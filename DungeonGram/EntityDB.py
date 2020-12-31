from os.path import join
from json import load

f = open(join('Assets', 'entities.json'))
edb_entities = load(f)
f.close()