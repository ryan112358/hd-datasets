import pandas as pd
import yaml
import json

config = json.load(open('fire-data-specs.json', 'r'))

out = {}

for col in config:
    info = config[col]
    print(info)
    curr = {}
    out[col] = curr
    if info['type'] == 'enum':
        curr['type'] = 'discrete'
        curr['bins'] = info['count']
        curr['domain'] = [0, info['count']-1]
    if info['type'] in ['integer', 'float']:
        curr['type'] = 'discrete'
        curr['bins'] = 100
        if info['optional']:
            curr['optional'] = True
        curr['domain'] = [info['min'], info['max']]

yaml.dump(out, open('config.yml', 'w'))
