#These are functions associated with preprocessing data.

import bz2
import pandas as pd
import numpy as np
import overpy
import os
from util.xmlTools import *
import time
# This takes in the file path of data and return a dataframe.
#This reads in the XML, it accepts path and returns a dataframe
def readXML(path, outpath, mp=12):
    startTime = time.time()
    #Opens the file from the path
    print(startTime)
    file = open(path).readlines()[3:]
    print(f"Input file was read in {startTime-time.time()} seconds")

    #Creates the dataframe

    if mp > 1:
        from multiprocessing import Pool
        # split the files
        splitFile = np.array_split(file, mp)

        # make sure we aren't missing any tags
        files = [list(splitFile[0])]
        for i,f in enumerate(splitFile[1:],1):
            n = 0
            for line in reversed(f):
                if getType(line) == 'tag':
                    files[i-1].append(line)
                    n -= 1
                else:
                    files.append(list(f[:n]))
                    break

        # read the chunks in with multiprocessing
        with Pool(mp) as p:
            out = p.map(readXMLChunk, files) 

        #ret = vstack(out)
        ret = pd.concat(out)

    else:
        ret = readXMLChunk(file)

    # add a column with if the node is an amenity        
    ret['hasAmenity'] = ['amenity' in row.tagKeys for ii,row in ret.iterrows()]
    
    # write out the pandas dataframe
    print(f'Writing cleaned XML file to {outpath}')
    ret.to_json(outpath)
    
    endTime = time.time()
    totalTime = endTime - startTime
    mins = totalTime // 60
    seconds = totalTime - (60 * mins)
    print(f"Time it took to run: {mins} minutes and {seconds} seconds")
    return ret
