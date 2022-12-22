import pandas as pd

g = pd.read_csv('gumayushi2.csv')
print(g)
w = pd.read_csv('Wayne2.csv')
g = g.dropna()
print(g)
w['player'] = w['player'].fillna(0)

res = pd.concat([g, w], axis = 0)

res.to_csv('opgg_enlarged.csv')
