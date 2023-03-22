'''
Explore the Cheapest Cars Dataset

Author: Noah Franz
'''

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/michaelcammarere/PycharmProjects/SCDV490-Final/data/Cheapestelectriccars-EVDatabase.csv')

print(df.keys())
print(df.Range)
print(df.Efficiency)


# plot histogram of ranges
fig, ax = plt.subplots()
ax.hist([int(line[:-3]) for line in df['Range']], bins=25)
ax.set_xlabel('Range [km]')
ax.set_ylabel('N')
fig.savefig('range-hist.png', bbox_inches='tight')

# plot histogram of efficiency
fig, ax = plt.subplots()
ax.hist([int(line[:-6]) for line in df['Efficiency']], bins=25)
ax.set_xlabel('Efficiency [Wh/km]')
ax.set_ylabel('N')
fig.savefig('efficiency-hist.png', bbox_inches='tight') 
