import pandas as pd

df = pd.read_csv(r'collection.csv')
df.to_json(r'collection.json')
