#These are functions associated with preprocessing data.

import pandas as pd
import numpy as np
import overpy
import os
from util.xmlTools import *
import time

# This takes in the file path of data and return a dataframe.
def getDataFrame(path):
    return pd.read_csv(path)

def readXML_Old(filepath):
    '''
    Reads an XML file from a Overpass query and outputs an overpy Result object

    filepath [str] : complete path to the XML file
    Returns : overpy.Result object
    '''

    # use the overpass API
    et = ET.parse(filepath)

    # start using overpy
    result = overpy.Result()
    result = result.from_xml(et.getroot(), parser=1)

    return result


#This reads in the XML, it accepts path and returns a dataframe
def readXML(path, mp=1):
    '''
    This reads the input path and then uses multiprocessing to read in chunks
    '''
    startTime = time.time()
    #Opens the file from the path
    file = np.array(open(path, 'r').readlines()[5:-2])
    print("Path has been read.")

    if mp == 1:
        ret = readXMLChunk(file)
    else:
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
        
        ret =  pd.concat(out)

    #Checking time of running
    endTime = time.time()
    totalTime = endTime - startTime
    mins = totalTime // 60
    seconds = totalTime - (60 * mins)
    print(f"Time it took to run: {mins} minutes and {seconds} seconds")

    return ret.reset_index(drop=True)
        
def readXMLChunk(file):

    #Creates the dataframe
    columns = ['type','id','lat','long','tags']
    df = pd.DataFrame(data=None, columns=columns)
    print("DataFrame has been created")
    
    #To avoid being above n time complexity, have to be a bit creative here.
    index = 0
    nNodes = 0
    while index < len(file)-1:
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
                tags = Tag(keys,values)
                #Updating the index
                index = newIndex
            else:
                tags = Tag([],[])
                index += 1
            data=[type,id,lat,long,tags]
            df.loc[len(df)] = data
        else:
            index += 1
        if index % 75000 == 0:
            print(f"The index is currently {index} out of {len(file)}")

    return df

    
