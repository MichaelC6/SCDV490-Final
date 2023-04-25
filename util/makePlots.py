'''
Generates a bunch of interesting plots for our analysis
'''
import os
import pickle
import glob
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
from mapFunctions import *

plt.style.use(os.path.join(os.getcwd(), 'charging-network.mplstyle'))

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
    '''
    Calculates the minimum distance between each node and it's nearest neighbor
    '''
    minSep = []
    for ii,row in df.iterrows():
        separations = geodesicDist(row.lat, row.long, np.array(df.lat), np.array(df.long))
        goodSeps = separations[separations > 0]
        minSep.append(min(separations))
    return np.array(minSep)

def plotMinDist(sep, outdir):
    '''
    Plots a histogram of the minimum separations
    '''
    fig, ax = plt.subplots()
    ax.hist(sep, bins=20, edgecolor='k')
    ax.set_ylabel('N')
    ax.set_xlabel('Minimum Separation [Miles]')
    ax.set_yscale('log')
    fig.savefig(os.path.join(outdir, 'min-sep-hist.png'))

def plotHeatMap(n, centers, outpath, **kwargs):
    '''
    Plots a heat map given nodes and centers
    '''

    lat = centers[:,0]
    long = centers[:,1]

    fig, ax = plt.subplots()
    im = ax.scatter(long, lat, c=n, marker='s', cmap='copper', norm=LogNorm())
    fig.colorbar(im, label='Number of Chargers')
    ax.set_ylabel('Latitude [deg]')
    ax.set_xlabel('Longitude [deg]')
    fig.savefig(outpath)
    
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

    minSeps = []
    nNodesPerState = []
    centersPerState = []
    for state in allStates:

        csvPath = os.path.join(os.getcwd(), 'data', 'csvs', f'{state}-out.csv')
        pklPath  = os.path.join(os.getcwd(), 'data', 'pickle', f'{state}-out.pkl')

        if not os.path.exists(csvPath) or not os.path.exists(pklPath):
            print(f'WARNING! Skipping {state} because the input files do not exist') 
            continue
            
        csv, nodes, centers = io(csvPath, pklPath)
        
        minSeps.append(distanceDifference(csv))

        if state in ['new-york', 'california', 'minnesota', 'rhode-island']:
            n = [len(row) for row in nodes]
            plotHeatMap(n, centers, os.path.join(outdir, state+'-heatmap.png'), s=25)

        # get info for heatmap by state
        nNodesPerState.append(len(csv))

        midIdx = (len(centers[:,1]) - 1)//2
        centerLat = np.sort(centers[:,0])[midIdx]
        centerLong = np.sort(centers[:,1])[midIdx]
        centersPerState.append([centerLat, centerLong])

    seps = np.concatenate(minSeps)
    plotMinDist(seps, outdir)

    plotHeatMap(np.array(nNodesPerState), np.array(centersPerState),
                os.path.join(outdir, 'US-heatmap.png'), s=100)
    
if __name__ == '__main__':
    main()