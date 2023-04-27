'''
Script to use the search software to simply run the search
'''

import os
import glob
import time
import pickle
from gen_charging_net import GenerateChargingNetwork
import pandas as pd

def getStateChargingNetwork(f, verbose=False):
    '''
    Get the charging network for a given state file
    '''

    # call the GenerateChargingNetwork software with the given file
    s = GenerateChargingNetwork(f)

    if verbose:
        print('json file data:')
        print(s.data)

    # generate the charging network now
    goodNodes = s.genChargingNetwork()

    # write goodNodes to a pickle file
    out = list(zip(s.gridCoordCenters.values(), goodNodes))

    # define some file paths
    outpkl = os.path.split(f)[-1].replace('-latest.json', '-out.pkl')
    outcsv = os.path.split(f)[-1].replace('-latest.json', '-out.csv')
    outdirpkl = os.path.dirname(f).replace('jsons', 'pickle')
    outdircsv = os.path.dirname(f).replace('jsons', 'csvs')
    if not os.path.exists(outdirpkl):
        os.makedirs(outdirpkl)
    if not os.path.exists(outdircsv):
        os.makedirs(outdircsv)

    # write out the pickle file with grid information
    outpath = os.path.join(outdirpkl, outpkl)
    with open(outpath, 'wb') as f:
        pickle.dump(out, f, pickle.HIGHEST_PROTOCOL)

    # write good nodes to a csv
    good = [item for item in goodNodes if len(item) > 0]
    allNodes = pd.concat(good)
    allNodes.to_csv(os.path.join(outdircsv, outcsv), header=True, index=False)

def main():

    # time it
    start = time.time()
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', help='JSON file path', default=None)
    args = parser.parse_args()
    
    if args.infile is None:
        infiledir = os.path.join(os.getcwd(), 'data', 'jsons')
        filenames = glob.glob(os.path.join(infiledir, '*.json'))
    else:
        infiledir = os.path.dirname(args.infile)
        filenames = [args.infile]

    # loop over all the JSON files (for each state)
    for filename in filenames:
        getStateChargingNetwork(filename)

    print(f'It took {time.time()-start} seconds to generate the charging network')
        
if __name__ == '__main__':
    main()
