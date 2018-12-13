import yaml
import pandas as pd
import numpy as np

seqs = []
with open('msnbc990928.seq', 'r') as f:
    for line in f:
        seqs.append([int(x) for x in line.split(' ')[:-1]])

max_length = 16
values = np.zeros((len(seqs), max_length), dtype=int)
for i, seq in enumerate(seqs):
    if len(seq) > max_length:
        values[i] = seq[:max_length]
    else:
        values[i,:len(seq)] = seq

cols = ['site_%d'%i for i in range(max_length)]

df = pd.DataFrame(data=values, columns=cols)

bins = 18
config = {}
for col in cols:
    config[col] = { 'bins' : 18, 'domain' : [0,17], 'type': 'discrete' }

yaml.dump(config, open('config.yml', 'w')) 
df.to_csv('data.csv', index=None)
