import os
import glob
import pandas as pd

results = glob.glob('*.csv')


big = set()

for file in results:
	new_df = pd.read_csv(file)
	big = big.union(set(new_df['product_id'].tolist()))

print(len(big))