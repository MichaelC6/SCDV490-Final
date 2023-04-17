'''
Class to hold software for the search algorithm. First attempt is DF
'''
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

        # read in the file with our XML parsing code
        self.data = readXML(self.filepath, stateName, mp)

        print(self.data)
        
        self.goodLocs = []
        
    def getRelevantNodes(self):
        '''
        Gets the relevant rows from self.data for the search

        FIX ME! WILL NEED TO TEST WITH LARGER DATASET
        '''

        goodRows = []
        for ii,row in self.data.iterrows():
            tag = row.tags
            if len(tag.keys) > 0: print(tag.keys)
            if 'amenity' in tag.keys:
                print(tag.keys, tag.values)
        
        

    def search(self, start=None, d=83.5, tol=1):
        '''
        Performs a search of nodes to find ideal locations of EV chargers

        start (tuple) : tuple in the form (latitude, longitude), default is random start
        d (float) : distance miles between EV chargers, default is 83.5
        tol (float) : distance in miles of tolerance on d, default is 1 

        return : DataFrame of ideal EV charger locations
        '''

        #self.getRelevantNodes()

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
            self.goodLocs.append(curr.to_frame().T)

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
