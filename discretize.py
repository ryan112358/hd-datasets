import pandas as pd
import yaml
import json
from pandas.api.types import CategoricalDtype
from IPython import embed
import argparse

def process(path, config):
    df = pd.read_csv(path)
    config = yaml.load(open(config, 'r'))
    domain = { } 
    for col in config:
        info = config[col]
        domain[col] = info['bins']
        if info['type'] == 'discrete':
            bins = info['bins']
            low, high = info['domain']
            buckets = pd.interval_range(low, high+1, bins, closed='left')
            df[col] = pd.cut(df[col], buckets)
        if info['type'] == 'categorical':
            categories = list(info['value_map'].keys())
            dtype = CategoricalDtype(categories, ordered=True)
            df[col] = df[col].astype(dtype)
    cols = list(config)
    discrete = df[cols].apply(lambda c: c.cat.codes)
    for col in cols:
        info = config[col]
        if 'optional' in info and info['optional']: # give missing data special value
            discrete[col] = discrete.replace(-1, domain[col])
            domain[col] += 1
        else: # remove missing data
            discrete = discrete[discrete[col] != -1]

    return discrete, domain

def default_params():
    """
    Return default parameters to run this program

    :returns: a dictionary of default parameter settings for each command line argument
    """
    params = {}
    params['folder'] = 'adult'
    return params


if __name__ == '__main__':
    from functools import reduce

    description = ''
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)
    parser.add_argument('folder', help='folder to discretize data from')

    parser.set_defaults(**default_params()) 
    args = parser.parse_args()
    
    folder = args.folder

    df, domain = process('raw/%s/data.csv' % folder, 'raw/%s/config.yml' % folder)
    df.to_csv('clean/%s.csv' % folder, index=False)
    json.dump(domain, open('clean/%s-domain.json' % folder, 'w'))

    print('%d total records' % df.shape[0])
    print('%0.2e domain size' % reduce(lambda x,y: x*y, domain.values()))
