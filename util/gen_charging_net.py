'''
Class to hold software for the search algorithm. First attempt is DF
'''
import os, ast
from util.preProcessing import readXML
from util.mapFunctions import *
import numpy as np
import pandas as pd
from copy import deepcopy

class GenerateChargingNetwork():

    def __init__(self, filepath, stateName, mp=16):
        '''
        filepath [str] : path to XML file to parse
        '''

        self.filepath = filepath

        outpath = os.path.join(os.path.split(self.filepath)[0], f'{stateName}-preprocessed.json')
        # read in the file with our XML parsing code
        if os.path.exists(outpath):
            print('Output file exists, reading in the data!') 
            self.data = pd.read_json(outpath)
        else:
            raise IOError('Please run getAllData before starting to generate the charging network')
            
        self.goodLocs = []
        self.grid = None
        self.gridCoordCenters = None

    def genChargingNetwork(self, mp=1):
        '''
        Create and return the locations of the nodes in the charging network
        '''
        self._gridData()

        if mp > 1:
            from multiprocessing import Pool
            with Pool(mp) as p:
                out = p.starmap(self._searchInBox, self.grid.values())

        else:
            mapOutput = map(self._searchInBox, self.grid.values())
            out = list(mapOutput)
            
        return out
        
    def _searchInBox(self, boxVals, start=None, percent=0.25):
        '''
        Performs a search of nodes to find ideal locations of EV chargers

        start (tuple) : tuple in the form (latitude, longitude), default is random start
        boxKey (int) : integer number describing the box
        boxVals (list): list of nodes in the box
        percent (float): percent of nodes in the box to randomly choose to place a charger at
        
        return : list of list of Nodes to place at (or None)
        '''

        # check length of nodes in the grid
        if len(boxVals) == 0:
            return pd.DataFrame({})

        n = int(np.ceil(len(boxVals)*percent))
        idxs = np.arange(0, len(boxVals), 1, dtype=int)

        # choose n random idxs
        chargerIdxs = np.random.choice(idxs, size=n, replace=False)
        
        return boxVals.iloc[chargerIdxs]
                
    def _getRelevantNodes(self):
        '''
        Gets the relevant rows from self.data for the search
        '''
        self.data = self.data[self.data.hasAmenity == True].reset_index(drop=True)  
        print(self.data)

    def _gridData(self, tileWidth=5):
        '''
        Creates a 2D grid of locations on the map where each item inside the outer dictionary
        is a pandas dataframe

        returns: dictionary where keys are the tile number
        '''

        self._getRelevantNodes()

        gridCoords = {}
        grid = {}
        #tileWidth = 5 # make each box in the grid a 5x5 mile box

        # coordinates of the box
        bottomLeft = (self.data.lat.min(), self.data.long.min())
        bottomRight = (self.data.lat.min(), self.data.long.max())
        topLeft = (self.data.lat.max(), self.data.long.min())
        topRight = (self.data.lat.max(), self.data.long.max())

        # start at bottom left corner
        currLong = bottomLeft[1]
        currLat = bottomLeft[0]
        origCurrLat = currLat
        print(f'Bottom left corner: {bottomLeft}')
        print(f'Bottom right corner: {bottomRight}')
        print(f'top left corner: {topLeft}')
        print(f'top right corner: {topRight}')

        mapWidth = geodesicDist(bottomLeft[0], bottomLeft[1], bottomRight[0], bottomRight[1])
        mapHeight = geodesicDist(bottomLeft[0], bottomLeft[1], topLeft[0], topLeft[1])
        
        ii = 0
        currWidth = 0
        while currWidth < mapWidth:
            currHeight = 0
            while currHeight < mapHeight:
                # calculate the distances from the currentLatitude and current Longitude for every node
                dist = geodesicDist(currLat, currLong, np.array(self.data.lat), np.array(self.data.long))
                inGrid = np.where(dist < tileWidth)[0]

                grid[ii] = self.data.iloc[inGrid]
                ii += 1

                gridCoords[ii] = [coordFromRadialDist(currLat, currLong, tileWidth/2, lon2=currLong),
                                  coordFromRadialDist(currLat, currLong, tileWidth/2, lat2=currLat)]
                
                currHeight += tileWidth
                currLat = coordFromRadialDist(currLat, currLong, tileWidth, lon2=currLong)

            currWidth += tileWidth
            currLong = coordFromRadialDist(currLat, currLong, tileWidth, lat2=currLat)
            currLat = origCurrLat

        self.grid = grid
        self.gridCoordCenters = gridCoords
        
