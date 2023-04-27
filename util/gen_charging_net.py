'''
Class to hold software for the search algorithm. First attempt is DF
'''
import os, time
from mapFunctions import *
import numpy as np
import pandas as pd
from copy import deepcopy

class GenerateChargingNetwork():

    def __init__(self, filepath):
        '''
        filepath [str] : path to XML file to parse
        '''

        self.filepath = filepath

        # read in the file with our XML parsing code
        if os.path.exists(filepath):
            start = time.time()
            print('Reading in the data!') 
            self.data = pd.read_json(filepath)
            print(f'It took {time.time()-start:.4f} to read in the data')
        else:
            raise IOError('Please run getAllData before starting to generate the charging network')
            
        self.grid = None # the data after being split into a grid
        self.gridCoordCenters = None # the centers of each grid location for analysis later

    def genChargingNetwork(self):
        '''
        Create and return the locations of the nodes in the charging network
        '''
        self._gridData()

        # generate the charging network by looping over self.grid
        # "map" loops overself.grid
        mapOutput = map(self._searchInBox, [*self.grid])

        out = list(mapOutput)
            
        return out
        
    def _searchInBox(self, idx, percent=0.25):
        '''
        Performs a search of nodes to find ideal locations of EV chargers

        start (tuple) : tuple in the form (latitude, longitude), default is random start
        boxKey (int) : integer number describing the box
        boxVals (list): list of nodes in the box
        percent (float): percent of nodes in the box to randomly choose to place a charger at
        
        return : list of list of Nodes to place at (or None)
        '''

        boxVals = self.grid[idx]
        
        # check length of nodes in the grid
        if len(boxVals) == 0:
            return pd.DataFrame({})

        # number of chargers per grid box
        n = int(np.ceil(len(boxVals)*percent))
        idxs = np.arange(0, len(boxVals), 1, dtype=int)

        # choose n random idxs
        chargerIdxs = np.random.choice(idxs, size=n, replace=False)
        
        return boxVals.iloc[chargerIdxs]
                
    def _getRelevantNodes(self):
        '''
        Gets the relevant rows from self.data for the search
        '''
        # clean up the data and only get things that are amenities
        self.data = self.data[self.data.hasAmenity == True].reset_index(drop=True)  
        print(self.data)

    def _gridData(self, tileWidth=5):
        '''
        Creates a 2D grid of locations on the map where each item inside the outer dictionary
        is a pandas dataframe

        returns: dictionary where keys are the tile number
        '''

        self._getRelevantNodes() # get amenities

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

        # calculate the total map dimensions for the state
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

                # add this data to the grid
                grid[ii] = self.data.iloc[inGrid]
                gridCoords[ii] = [coordFromRadialDist(currLat, currLong, tileWidth/2, lon2=currLong),
                                  coordFromRadialDist(currLat, currLong, tileWidth/2, lat2=currLat)]

                # recalculate the current latitude
                currHeight += tileWidth
                currLat = coordFromRadialDist(currLat, currLong, tileWidth, lon2=currLong)

                ii += 1

            # update the current width
            currWidth += tileWidth
            currLong = coordFromRadialDist(currLat, currLong, tileWidth, lat2=currLat)
            currLat = origCurrLat

        # assign grid to instance variable
        self.grid = grid
        self.gridCoordCenters = gridCoords
        
