import time
import multiprocessing as mp
import pandas as pd
import sys
import os
import glob
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from util.xmlTools import *
import numpy as np
    
def writeXML(args):
    section, outfile = args
    file = open(outfile, 'w', encoding='utf-8')
    file.writelines(section)
    file.close()

def getAllChunks():
    allChunksPath = os.path.join(os.getcwd(), "data", "temp")
    allChunks = os.listdir(allChunksPath)
    ret = []
    for file in allChunks:
        ret.append(os.path.join(allChunksPath, file))
    return ret

def chunkXML(path):
    #Opens the file from the path
    file = open(path).readlines()[3:]

    cores = mp.cpu_count() - 1

    numFiles = cores * 10

    indicies = np.linspace(0,len(file)-1,numFiles, dtype=int)

    newPath = os.path.join(os.getcwd(), "data", "temp")

    if not os.path.exists(newPath):
        os.makedirs(newPath)
        print("made new path")

    #for i in the length of the indicies

    for i in range(0,len(indicies[:-1])):

        endline = file[indicies[i + 1]]

        #If the current line is a tag OR the next line is a tag keep going up
        #If anything else it can split normally we do not care.
        while getType(endline) == 'tag':
            indicies[i + 1] += 1
            line = file[indicies[i]]
            endline = file[indicies[i + 1]]


    sections = []
    files = []

    for i,j in zip(indicies[:-1], indicies[1:]):
        sections.append(file[i:j])
        files.append(os.path.join(newPath, str(i) + "-" + str(j) + ".osm"))
    
    print("got each file indicies")

    file = None

    #Now we need to export each file
    
    args = []
    for s,f in zip(sections,files):
        args.append([s,f])

    return args

if __name__ == '__main__':

    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--filename', help='filename to convert from .osm to .json')
    p.add_argument('--allStates', dest='allStates', action='store_true', help='should we run on all states?')
    p.set_defaults(allStates=False)
    args = p.parse_args()

    dataFolder = os.path.join(os.getcwd(), "data")
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
    
    if not args.allStates:
        filenames = [args.filename]
    else:
        filenames = glob.glob(dataFolder+'*.osm')

    for filename in filenames:

        jsonName = filename.split('.')[0] + '.json'
    
        startTime = time.time()
    
        filePath = os.path.join(dataFolder, filename)
        
        jsonPath = os.path.join(dataFolder, "jsons")
    
        if not os.path.exists(jsonPath):
            os.makedirs(jsonPath)
            print("made new path")
    
        args = chunkXML(filePath)
        cores = mp.cpu_count() - 1
        with mp.Pool(cores) as p:
            p.map(writeXML, args) 
            p.close()
        print("Finished Splitting")

        allChunks = getAllChunks()
        p = mp.Pool(cores)
        out = p.map(readXMLChunk, allChunks)
        ret = pd.concat(out)
        ret.reset_index(inplace=True)
        p.close()

        ret['hasAmenity'] = ['amenity' in row.tagKeys for ii,row in ret.iterrows()]
    
        # write out the pandas dataframe
        print(f'Writing cleaned XML file to {os.path.join(jsonPath, jsonName)}')

        ret.to_json(os.path.join(jsonPath, jsonName))
        print("Finished Processing")

        for c in allChunks:
            os.remove(c)
        os.rmdir(os.path.join(dataFolder, 'temp'))
        print("Deleted Temp")

        endTime = time.time()
        totalTime = endTime - startTime
        mins = totalTime // 60
        seconds = totalTime - (60 * mins)
        print(f"Time it took to run: {mins} minutes and {seconds} seconds")
