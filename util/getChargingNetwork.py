'''
Script to use the search software to simply run the search
'''

import os
import time
import pickle
from util.gen_charging_net import GenerateChargingNetwork

def getStateChargingNetwork(f, verbose=False):

    s = GenerateChargingNetwork(args.infile)

    if verbose:
        print('json file data:')
        print(s.data)
    
    goodNodes = s.genChargingNetwork()

    # write goodNodes to a pickle file
    out = list(zip(s.gridCoordCenters.values(), goodNodes))

    outfile = os.path.split(args.infile)[-1].replace('-latest.json', '-out.pkl')
    outdir = os.path.dirname(args.infile).replace('jsons', 'pickle')
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    outpath = os.path.join(outdir, outfile)
    with open(outpath, 'wb') as f:
        pickle.dump(out, f, pickle.HIGHEST_PROTOCOL)


def main():

    start = time.time()
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', help='JSON file path', default=None)
    args = parser.parse_args()
    
    if args.infile is None:
        infiledir = os.path.join(os.getcwd(), 'data', 'jsons')
        filenames = glob.glob(infiledir+'*.json')
    else:
        infiledir = os.path.dirname(args.infile)
        filenames [args.infile]

    for filename in filenames:
        getStateChargingNetwork(filename)

    print(f'It took {time.time()-start} seconds to generate the charging network')
        
if __name__ == '__main__':
    main()
