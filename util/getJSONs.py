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
import json
    
def writeXML(args):
    section, outfile = args
    file = open(outfile, 'w', encoding='utf-8')
    file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    file.write("<osm version=\"0.6\" generator=\"osmium/1.14.0\">\n")
    file.writelines(section)
    file.write("</osm>\n")
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
    file = open(path, encoding='utf-8').readlines()[3:]

    cores = mp.cpu_count()

    numFiles = cores - 1

    indicies = np.linspace(0,len(file)-1,numFiles+1, dtype=int)

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
    files = []

    for i,j in zip(indicies[:-1], indicies[1:]):
        files.append(os.path.join(os.getcwd(),"data","osm","temp",f"{i}-{j}.osm"))
    

    sNum = 0    
    temp = open(files[sNum], 'w', encoding='utf-8')
    for index,line in enumerate(file):
        if index >= indicies[sNum] and index < indicies[sNum + 1]:
            temp.write(line)
        else:
            if index == len(file)-1:
                temp.write(line)
                temp.close()
                del temp
                gc.collect()
            else:
                temp.close()
                del temp
                gc.collect()
                sNum += 1
                temp = open(files[sNum], 'w', encoding='utf-8')
                temp.write(line)

    del file
    gc.collect()

    print("got each file indicies and have written to temp")

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
        
        # args = chunkXML(filePath)
        # print(f"The Length of section: {len(args[0][0])}")
        # print(f"The Length of section: {len(args[1][0])}")
        # print(f"The Length of section: {len(args[-1][0])}")
        # cores = mp.cpu_count() - 1
        # for arg in args:
        #     writeXML(arg)
            
        # print("Finished Splitting")
        # del args
        # gc.collect()

        # chunkXML(filePath)
        # file = None
        # cores = mp.cpu_count() - 1
        # allChunks = getAllChunks()
        # p = mp.Pool(cores)
        # out = p.map(readXMLChunk, allChunks)
        # ret = pd.concat(out)
        # ret.reset_index(inplace=True)
        # p.close()

        ret = readXMLChunk(filePath)

        ret['hasAmenity'] = ['amenity' in row.tagKeys for ii,row in ret.iterrows()]
    
        # write out the pandas dataframe
        print(f'Writing cleaned XML file to {jsonFilePath}')

        ret.to_json(jsonFilePath)
        print("Finished Processing")

        # for c in allChunks:
        #     os.remove(c)
        # os.rmdir(os.path.join(dataFolder, 'temp'))
        # print("Deleted Temp")

        endTime = time.time()
        totalTime = endTime - startTime
        mins = totalTime // 60
        seconds = totalTime - (60 * mins)
        print(f"Time it took to parse {filename}: {mins} minutes and {seconds} seconds")
