'''
Class to hold software for the search algorithm. First attempt is DF
'''
import os, ast
from util.preProcessing import readXML
from util.mapFunctions import geodesicDist
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
        
    def getRelevantNodes(self):
        '''
        Gets the relevant rows from self.data for the search
        '''
        self.data['hasAmenity'] = ['amenity' in row.tagKeys for ii,row in self.data.iterrows()]
        self.data = self.data[self.data.hasAmenity == True].reset_index(drop=True)  
        print(self.data)
        
    def search(self, start=None, d=83.5, tol=1):
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

        idx = startIdx
        locs = deepcopy(self.data)
        
        while True:
            #print(type(curr.to_frame()), curr.to_frame())
            self.goodLocs.append(curr.to_frame().transpose())

            # remove row from input dataframe to prevent loops
            locs = locs.drop(index=idx).reset_index(drop=True)
            
            # calculate the distances
            dist = np.array(geodesicDist(curr.lat, curr.long, locs.lat, locs.long))

            # find indexes that are close
            sep = np.abs(dist-d)
            m = np.min(sep)
            idx = np.where(m == sep)[0][0]
            #print(m, idx)
            if sep[idx] < tol:
                curr = locs.iloc[idx]
            else:
                print(f'Minimum seperation found: {m} miles')
                print(f'No nodes found within {d} miles so search is done!')
                break

        self.goodLocs = pd.concat(self.goodLocs)
