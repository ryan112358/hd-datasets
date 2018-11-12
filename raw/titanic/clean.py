import pandas as pd

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
cols = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Cabin', 'Embarked', 'Survived']

data = pd.concat([train[cols], test[cols]])
data['Cabin'] = data['Cabin'].str[0]

data.to_csv('data.csv')
