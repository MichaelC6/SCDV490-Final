#These are functions associated with preprocessing data.

import bz2
import pandas as pd
from astropy.table import Table, vstack
from astropy.io.misc.hdf5 import write_table_hdf5
import numpy as np
import overpy
import os
from util.xmlTools import *
import time

# This takes in the file path of data and return a dataframe.
#This reads in the XML, it accepts path and returns a dataframe
def readXML(path, stateName, mp=12):
    startTime = time.time()
    #Opens the file from the path
    file = bz2.open(path, 'r').readlines()[3:]
    print("Path has been read.")

    #Creates the dataframe
    columns = ['type','id','lat','long','tags']
    #df = pd.DataFrame(data=None, columns=columns)
    df = {}

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
        
        ret =  vstack(out)

    else:
        ret = readChunk(file)
    
    # write out the astropy table
    #print(f'Writing cleaned XML file to {stateName}-nodes.h5')
    #write_table_hdf5(df, '{stateName}-nodes.h5')
    
    endTime = time.time()
    totalTime = endTime - startTime
    mins = totalTime // 60
    seconds = totalTime - (60 * mins)
    print(f"Time it took to run: {mins} minutes and {seconds} seconds")
    return df


def readXMLChunk(file):
    '''
    Read a small chunk of the state dataset

    file : open file object
    '''

    #To avoid being above n time complexity, have to be a bit creative here.
    index = 0
    nNodes = 0
    while index < len(file):
        #print(f"CURRENT INDEX: {index}")
        #Starts by getting the current line
        line = file[index]
        #Then it gets the type of the current line
        type = getType(line)
        #print(f"THE TYPE: {type}")
        #If the type is a node, it gets all the info it needs
        if type == 'node':
            nNodes += 1
            id, lat, long = readNode(line)
        #Then if the next row is a tag
            if getType(file[index+1]) == 'tag':
                #print("IN A TAG!")
                #Go to the next row and get the line
                index += 1
                line = file[index]
                #Use the readAllTags function
                keys,values,newIndex = readAllTags(file,index)
                #And return the tag type
                if len(keys) != len(values):
                    raise Exception('number of keys and values is different!')
                tags = {key:value for key, value in zip(keys, values)}
                #Updating the index
                index = newIndex
            else:
                tags = {} #Tag([],[])
                index += 1
            data=[type,id,lat,long,tags]
            df[nNodes] = data
            #df.loc[len(df)] = data
        else:
            index += 1
        if index % 1000000 == 0:
            print(f"The index is currently {index} out of {len(file)}")

    #Checking time of running
    df = Table(df)

    return df
