'''
Script to use the search software to simply run the search
'''

import os
from classes.gen_charging_net import GenerateChargingNetwork

def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', help='in file path', required=True)
    args = parser.parse_args()

    stateName = os.path.split(args.infile)[-1].replace('-latest.osm', '')
    s = GenerateChargingNetwork(args.infile, stateName, mp=1)
    
    print(s.data)
    
    goodNodes = s.genChargingNetwork()

    print(goodNodes)
if __name__ == '__main__':
    main()
