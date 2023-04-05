#These are functions associated with preprocessing data.

import pandas as pd
import overpy
import os
from xmlTools import *

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
def readXML(path):
    #Opens the file from the path
    file = open(path, 'r').readlines()[5:-2]

    #Creates the dataframe
    columns = ['type','id','lat','long','tags']
    df = pd.DataFrame(data=None, columns=columns)

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
    return df

    
