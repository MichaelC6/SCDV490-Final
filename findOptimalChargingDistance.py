'''
Script to determine the optimal distance between chargers based
on current electric car distance data (as of spring 2023)
'''

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in and clean the data
# this data is from https://afdc.energy.gov/data/10963
filepath = os.path.join(os.getcwd(), 'sampleData', 'EV_range_efficiency.csv')
ranges = pd.read_csv(filepath, skiprows=2)

ranges = ranges.dropna(how='all', axis=1)
ranges = ranges.dropna(how='all', axis=0)

# let's histogram all the ranges and add vertical lines at the quartiles
