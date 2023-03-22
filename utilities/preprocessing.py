#These are functions associated with preprocessing data.

import pandas as pd

# This takes in the file path of data and return a dataframe.
def getDataFrame(path):
    return pd.read_csv(path)