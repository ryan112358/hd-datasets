import pandas as pd
import yaml
from collections import OrderedDict
from math import ceil

data = pd.read_csv('loans.csv')

for col in data:
    if not pd.notnull(data[col]).any():
        del data[col]

del data['pymnt_plan'], data['desc'], data['title'], data['initial_list_status']
del data['out_prncp'], data['out_prncp_inv'], data['hardship_flag']
del data['policy_code'], data['application_type'], data['disbursement_method']
del data['collections_12_mths_ex_med'], data['chargeoff_within_12_mths']
del data['emp_title'], data['tax_liens'], data['acc_now_delinq']

# ept_title, issue_d, zip

data['int_rate'] = data.int_rate.str.strip('%').astype(float)
data['earliest_cr_line'] = data.earliest_cr_line.str[4:] # convert mon-year to year
data['revol_util'] = data.revol_util.str.strip('%').astype(float).max()
data['loan_amnt'] = data.loan_amnt.astype(float)
data['funded_amnt'] = data.funded_amnt.astype(float)
data['revol_bal'] = data.revol_bal.astype(float)

data.to_csv('data.csv', index=False)

for curr in [int, float, object]:
    for col in data:
        dtype = data[col].dtype
        if dtype == curr:
            if dtype == int:
                print(col, dtype, data[col].min(), data[col].max())
            if dtype == float:
                print(col, dtype, data[col].min(), data[col].max())
            if dtype == object:
                vals = data[col].value_counts()
                print(col, dtype, len(vals))
    print('\n')

bounds = {}
bounds['loan_amnt'] = 35000
bounds['funded_amnt'] = 35000
bounds['funded_amnt_inv'] = 35000
bounds['int_rate'] = 25
bounds['installment'] = 1500
bounds['annual_inc'] = 500000
bounds['dti'] = 30
bounds['delinq_2yrs'] = 15
bounds['inq_last_6mths'] = 25
bounds['mths_since_last_delinq'] = 120
bounds['mths_since_last_record'] = 132
bounds['open_acc'] = 60
bounds['pub_rec'] = 5
bounds['revol_bal'] = 1000000
bounds['revol_util'] = 120
bounds['total_acc'] = 100
bounds['total_pymnt'] = 70000
bounds['total_pymnt_inv'] = 70000
bounds['total_rec_prncp'] = 35000
bounds['total_rec_int'] = 35000
bounds['total_rec_late_fee'] = 250
bounds['recoveries'] = 35000
bounds['collection_recovery_fee'] = 10000
bounds['last_pymnt_amnt'] = 35000
bounds['delinq_amnt'] = 10000
bounds['pub_rec_bankruptcies'] = 2
bounds['settlement_amount'] = 15000
bounds['settlement_percentage'] = 100
bounds['settlement_term'] = 24

bins = {}
bins['delinq_2yrs'] = 16
bins['inq_last_6mths'] = 26
bins['mths_since_last_delinq'] = 121
bins['mths_since_last_record'] = 121
bins['open_acc'] = 61
bins['pub_rec'] = 6
bins['revol_util'] = 121
bins['pub_rec_bankruptcies'] = 3
bins['settlement_term'] = 25

config = {}
out = open('config.yml', 'w')
for col in data:
    dtype = data[col].dtype
    if dtype == float:
        b = bins[col] if col in bins else 32
        curr = { 'type' : 'discrete', 
                 'bins' : b, 
                 'optional' : True,
                 'domain' : [0, bounds[col]] }
        yaml.dump({ col : curr }, out)

values = {}
values['zip_code'] = ['{0:0=3d}xx'.format(d) for d in range(1000)]
values['issue_d'] = ['%s-%s'%(m,y) for y in [2007,2008,2009,2010,2011] for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
values['earliest_cr_line'] = [str(x) for x in range(1940, 2011)]
values['last_pymnt_d'] = ['%s-%s'%(m,y) for y in [2007,2008,2009,2010,2011] for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
values['next_pymnt_d'] = ['%s-%s'%(m,y) for y in [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016] for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
values['last_credit_pull_d'] = ['%s-%s'%(m,y) for y in [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018] for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
values['debt_settlement_flag_date'] = ['%s-%s'%(m,y) for y in [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018] for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
values['settlement_date'] = ['%s-%s'%(m,y) for y in [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018] for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]

for col in data:
    dtype = data[col].dtype
    if dtype == object:
        if col in values:
            vals = values[col]
        else:
            vals = sorted(data[col].dropna().unique())
        curr = { 'type' : 'categorical',
                 'bins' : len(vals),
                 'optional' : True,
                 'value_map' : dict(zip(vals, range(len(vals)))) }
        yaml.dump({ col : curr }, out)

out.close()
