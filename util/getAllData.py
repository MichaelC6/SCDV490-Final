#This is a function to get map data for every state
from subprocess import run
import wget
import os
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', help='output directory', default=None)
    parser.add_argument('--state', help='download one state', default=None)
    args = parser.parse_args()
    
    path = args.outdir
    specificState = args.state

    if path is None:
        path = os.getcwd()
        print(f'WARNING! outputting files to your current working directory: {path}')

    if not os.path.exists(path):
        os.makedirs(path)

    allStates = ["alabama","arizona","arkansas","california","colorado","connecticut","delaware",
                 "district-of-columbia","florida","georgia","idaho","illinois","indiana","iowa",
                 "kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan","minnesota",
                 "mississippi","missouri","montana","nebraska","nevada","new-hampshire","new-jersey","new-mexico",
                 "new-york","north-carolina","north-dakota","ohio","oklahoma","oregon","pennsylvania",
                 "rhode-island","south-carolina","south-dakota","tennessee","texas",
                 "utah","vermont","virginia","washington","west-virginia","wisconsin","wyoming"]
    
    if specificState is not None:
        if specificState not in allStates:
            raise IOError('You provided {specificState} which is invalid. Please provide a valid input state!')
        allStates = [specificState]

    link = "https://download.geofabrik.de/north-america/us/"
    
    for state in allStates:
        stateLink = link + state + "-latest.osm.bz2"
        filePath = os.path.join(path, state + "-latest.osm.bz2")
        outfile = os.path.join(path, state + "-latest.osm")

        if os.path.exists(outfile):
            print(f'WARNING! Skipping {stateLink} because the output already exists')
            continue
            
        print(f'Downloading {stateLink}')
        wget.download(stateLink,filePath)

        print(f'Unpacking {filePath}')
        run(f'bunzip2 {filePath}', shell=True)

if __name__ == '__main__':
    main()
