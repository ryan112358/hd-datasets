import pandas as pd
import yaml
import numpy as np

df = pd.read_csv('2to16disabilityNLTCS/2to16disabilityNLTCS.txt', delimiter='\t')

active = df.values[:,:16]
counts = df.values[:,16].astype(int)

values = np.repeat(active, counts, axis=0)[:,::-1]
cols = ['eating', 'getting in/out of bed', 'getting around inside', 'dressing', 'bathing', 'using toilet', 'heavy house work', 'light house work', 'laundry', 'cooking', 'grocery shopping', 'getting about outside', 'traveling', 'managing money', 'taking medicine', 'telephoning']
#cols = ['Y%d' % d for d in range(1,17)]

np.random.shuffle(values)
data = pd.DataFrame(values, columns = cols)

data.to_csv('data.csv', index=False)

config = {}
for c in cols:
    config[c] = { 'type' : 'discrete', 'bins' : 2, 'domain' : [0,1] }

yaml.dump(config, open('config.yml', 'w')) 
