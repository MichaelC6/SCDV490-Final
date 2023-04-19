'''
Class to hold software for the search algorithm. First attempt is DF
'''
import os, ast
from util.preProcessing import readXML
from util.mapFunctions import *
import numpy as np
import pandas as pd
from copy import deepcopy

class Search():

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
            print('Output file does not exist, cleaning the input file')
            self.data = readXML(self.filepath, outpath, mp)
            
        self.goodLocs = []
        self.grid = None
        
    def getRelevantNodes(self):
        '''
        Gets the relevant rows from self.data for the search
        '''
        self.data = self.data[self.data.hasAmenity == True].reset_index(drop=True)  
        print(self.data)

    def gridData(self):
        '''
        Creates a 2D grid of locations on the map where each item inside the outer dictionary
        is a pandas dataframe

        returns: dictionary where keys are the tile number
        '''

        self.getRelevantNodes()
        
        grid = {}
        tileWidth = 5 # make each box in the grid a 5x5 mile box

        # coordinates of the box
        bottomLeft = (self.data.long.min(), self.data.lat.min())
        bottomRight = (self.data.long.max(), self.data.lat.min())
        topLeft = (self.data.long.min(), self.data.lat.max())
        topRight = (self.data.long.max(), self.data.lat.max())

        # start at bottom left corner
        currLong = bottomLeft[0]
        currLat = bottomLeft[1]
        origCurrLat = currLat
        print(f'Bottom left corner: ({currLat}, {currLong})')

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

                currHeight += tileWidth
                currLat = coordFromRadialDist(currLat, currLong, tileWidth, lon2=currLong)

            currWidth += tileWidth
            currLong = coordFromRadialDist(currLat, currLong, tileWidth, lat2=currLat)
            currLat = origCurrLat

        self.grid = grid
                
    def searchInBox(self, start=None, d=83.5, tol=1):
        '''
        Performs a search of nodes to find ideal locations of EV chargers

        start (tuple) : tuple in the form (latitude, longitude), default is random start
        d (float) : distance miles between EV chargers, default is 83.5
        tol (float) : distance in miles of tolerance on d, default is 1 

        return : DataFrame of ideal EV charger locations
        '''

        self.getRelevantNodes()

        # get random starting location if start is None
        if start is None:
            startIdx = np.random.randint(len(self.data))
            curr = self.data.iloc[startIdx]
        else:
            startIdx = self.data.index[(self.data.lat == start[0]) * (self.data.long == start[1])]
            curr = self.data.iloc[startIdx]

        
