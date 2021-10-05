import yaml
import pandas as pd
import numpy as np

data = pd.read_csv('data.csv')

exceptions = ['FU1_RECD', 'FU2_DONE']

config = {}

for col in data:
    if col in exceptions:
        continue
    curr = {}
    config[col] = curr
    dtype = data[col].dtype
    d = data[col]
    if not d.notnull().all():
        curr['optional'] = True
    if dtype == int:
        curr['type'] = 'discrete'
        curr['domain'] = [int(d.min()), int(d.max())]
        curr['bins'] = int(min(32, d.max() - d.min() + 1))
    if dtype == float:
        curr['type'] = 'discrete'
        curr['domain'] = [float(d.min()), float(d.max())]
        curr['bins'] = 32
    if dtype == object:
        print(col)
        curr['type'] = 'categorical'
        unique = d.dropna().unique()
        curr['domain'] = [0, len(unique)-1]
        curr['bins'] = len(unique)
        curr['value_map'] = dict(zip(sorted(unique), range(len(unique))))

yaml.dump(config, open('config.yml', 'w'))
