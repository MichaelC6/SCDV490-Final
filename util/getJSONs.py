import time
import multiprocessing as mp
import pandas as pd
import sys
import os
import glob
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from util.xmlTools import *
import numpy as np
import itertools
import gc
    
def writeXML(args):
    section, outfile = args
    file = open(outfile, 'w', encoding='utf-8')
    file.writelines(section)
    file.close()
    del file
    gc.collect()


def getAllChunks():
    allChunksPath = os.path.join(os.getcwd(), "data", "osm", "temp")
    allChunks = os.listdir(allChunksPath)
    ret = []
    for file in allChunks:
        ret.append(os.path.join(allChunksPath, file))
    return ret

def chunkXML(path):
    #Opens the file from the path
    file = open(path).readlines()[3:]

    cores = 5

    numFiles = mp.cpu_count() - 1

    indicies = np.linspace(3,len(file)-1,numFiles+1, dtype=int)

    newPath = os.path.join(os.getcwd(), "data", "osm", "temp")

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

    # once indicies are adjusted we no longer need the file and can kill it 
    del file
    gc.collect()

    file = open(path)
    sectionIndex = 0
    files = []
    barriers = list(zip(indicies[:-1], indicies[1:]))
    lastBarrier = len(barriers) - 1
    sections = [[]] * numFiles
    index = 3
    bBar,eBar = barriers[sectionIndex]
    for line in file:
        if index >= bBar and index < eBar:
            sections[sectionIndex].append(line)
            index += 1
        else:
            if index == barriers[lastBarrier][1]:
                sections[-1].append(line)
                files.append(os.path.join(newPath, str(bBar) + "-" + str(eBar) + ".osm"))
            else:
                #print(f"SINDEX: {sectionIndex} OUT OF {len(barriers)-1}")
                #print(f"THE INDEX IS {index} out of {barriers[lastBarrier]}")
                files.append(os.path.join(newPath, str(bBar) + "-" + str(eBar) + ".osm"))
                sectionIndex += 1
                bBar,eBar = barriers[sectionIndex]
                sections[sectionIndex].append(line)
                index += 1
    
    file.close()
    del file
    gc.collect()

    print("got each file indicies")

    #Now we need to export each file    

    return list(zip(sections,files))

if __name__ == '__main__':

    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--filename', help='filename to convert from .osm to .json')
    p.add_argument('--allStates', dest='allStates', action='store_true', help='should we run on all states?')
    p.add_argument('--overwrite', dest='overwrite', action='store_true', help='should we overwrite existing files?')
    p.set_defaults(allStates=False)
    p.set_defaults(overwrite=False)
    args = p.parse_args()
    
    dataFolder = os.path.join(os.getcwd(), "data", "osm")
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
    
    if not args.allStates:
        filenames = [args.filename]
    else:
        filenames = glob.glob(os.path.join(dataFolder, '*.osm'))

    jsonPath = os.path.join(os.getcwd(),"data","jsons")
    if not os.path.exists(jsonPath):
        os.makedirs(jsonPath)
        print("made new path")
    
    for filename in filenames:
        print(f"CURRENTLY DOING {filename}")
        jsonName = filename.split("/")[-1].split('.')[0] + '.json'
        print(jsonName)
        print(f"C DIRECT {os.getcwd()}")
        jsonFilePath = os.path.join(os.getcwd(),"data","jsons",jsonName)
        print(f"FILE PATH: {jsonFilePath}")
        if os.path.exists(jsonFilePath) and not args.overwrite:
            print(f'WARNING! Skipping {filename} because the json already exists')
            continue
            
        startTime = time.time()
    
        filePath = os.path.join(dataFolder, filename)
        
        args = chunkXML(filePath)
        cores = mp.cpu_count() - 1
        for arg in args:
            writeXML(arg)
        # with mp.Pool(cores) as p:
        #     p.map(writeXML, args) 
        #     p.close()
        print("Finished Splitting")
        del args
        gc.collect()

        allChunks = getAllChunks()
        p = mp.Pool(cores)
        out = p.map(readXMLChunk, allChunks)
        ret = pd.concat(out)
        ret.reset_index(inplace=True)
        p.close()

        ret['hasAmenity'] = ['amenity' in row.tagKeys for ii,row in ret.iterrows()]
    
        # write out the pandas dataframe
        print(f'Writing cleaned XML file to {jsonFilePath}')

        ret.to_json(jsonFilePath)
        print("Finished Processing")

        for c in allChunks:
            os.remove(c)
        os.rmdir(os.path.join(dataFolder, 'temp'))
        print("Deleted Temp")

        endTime = time.time()
        totalTime = endTime - startTime
        mins = totalTime // 60
        seconds = totalTime - (60 * mins)
        print(f"Time it took to parse {filename}: {mins} minutes and {seconds} seconds")