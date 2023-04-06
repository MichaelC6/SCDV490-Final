'''
Class to hold software for the search algorithm. First attempt is DFS
'''
from util.preProcessing import readXML
from util.mapFunctions import geodesicDist
import numpy as np
from copy import deepcopy

class Search():

    def __init__(self, filepath):
        '''
        filepath [str] : path to XML file to parse
        '''

        self.filepath = filepath

        # read in the file with our XML parsing code
        self.data = readXML(self.filepath, mp=8)

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
        
        

    def search(self, start=None, d=83.5):
        '''
        Performs a search of nodes to find ideal locations of EV chargers

        start (tuple) : tuple in the form (latitude, longitude), default is random start
        d (float) : distance between EV chargers, default is 83.5

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
        print(curr, locs)
        while True:
            print(idx)
            self.goodLocs.append(locs.iloc[idx])

            # remove row from input dataframe to prevent loops
            locs = locs.drop(index=idx)
            #print(curr, locs)
            # calculate the distances
            dist = geodesicDist(curr.lat, curr.long, locs.lat, locs.long)
            print(dist)
            break
        
