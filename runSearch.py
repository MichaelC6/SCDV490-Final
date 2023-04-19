'''
Script to use the search software to simply run the search
'''

import os
from classes.search import Search

def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', help='in file path', required=True)
    args = parser.parse_args()

    stateName = os.path.split(args.infile)[-1].replace('-latest.osm', '')
    s = Search(args.infile, stateName, mp=1)
    
    print(s.data)
    
    s.gridData()

    print(s.grid)
if __name__ == '__main__':
    main()
