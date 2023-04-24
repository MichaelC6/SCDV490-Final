'''
Generates a bunch of interesting plots for our analysis
'''
import os
import pickle
import glob
import matplotlib.pyplot as plt
import pandas as pd
from mapFunctions import *

def io(csvPath, pklPath):
    '''
    Reads in the given output csv file and pickle file
    '''
    csv = pd.read_csv(csvPath)

    with open(pklPath, 'rb') as f:
        data = np.array(pickle.load(f), dtype=object)

    centers = np.array([np.array(d) for d in data[:,0]])
    nodes = data[:,1]

    return csv, nodes, centers

def distanceDifference(df):

    

def main():

    outdir = os.path.join(os.getcwd(), 'data', 'plots')
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    allStates = ["alabama","arizona","arkansas","california","colorado","connecticut","delaware",
                 "district-of-columbia","florida","georgia","idaho","illinois","indiana","iowa",
                 "kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan","minnesota",
                 "mississippi","missouri","montana","nebraska","nevada","new-hampshire","new-jersey","new-mexico",
                 "new-york","north-carolina","north-dakota","ohio","oklahoma","oregon","pennsylvania",
                 "rhode-island","south-carolina","south-dakota","tennessee","texas",
                 "utah","vermont","virginia","washington","west-virginia","wisconsin","wyoming"]

    for state in allStates:

        csvPath = os.path.join(os.getcwd(), 'data', 'csvs', f'{stateName}-out.csv')
        pklPath  = os.path.join(os.getcwd(), 'data', 'pickle', f'{stateName}-out.pkl')

        if not os.path.exists(csvPath) or not os.path.exists(pklPath):
            print(f'WARNING! Skipping {state} because the input files do not exist') 
            continue
            
        csv, nodes, centers = io(csvPath, pklPath)

        

    
if __name__ == '__main__':
    main()
