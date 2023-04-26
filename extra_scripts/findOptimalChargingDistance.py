'''
Script to determine the optimal distance between chargers based
on current electric car distance data (as of spring 2023)
'''

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#sns.set_theme(context='talk', style='white', palette='Set1')
plt.style.use(os.path.join(os.getcwd(), 'charging-network.mplstyle'))

# read in and clean the data
# this data is from https://afdc.energy.gov/data/10963
dir = os.path.join(os.getcwd(), 'data', 'oldFiles')
filepath = os.path.join(dir, 'EV_range_efficiency.csv')
ranges = pd.read_csv(filepath, skiprows=2)

ranges = ranges.dropna(how='all', axis=1)
ranges = ranges.dropna(how='all', axis=0)

# let's histogram all the ranges and add vertical lines at the quartiles
fig, ax = plt.subplots()
ax.hist(ranges.Range, bins=15, edgecolor='k')
ax.set_ylabel('N')
ax.set_xlabel('Range (Miles)')

quantiles = ranges.Range.quantile([0.10,0.25,0.5,0.75,0.90])
ax.axvline(quantiles.iloc[4], linestyle='--', color='k', label='3rd Quartile')
ax.axvline(quantiles.iloc[2], linestyle=':', color='k', label='Median')
ax.axvline(quantiles.iloc[1], linestyle='-.', color='k', label='1st Quartile')

ax.legend()

fig.savefig('range-hist.png', bbox_inches='tight', transparent=False)

# write quartiles out to a file
quantiles.to_csv(os.path.join(dir, 'range-quantiles.csv'))
print(f'I would recommend using the 25% limit at {quantiles.iloc[1]} miles')
