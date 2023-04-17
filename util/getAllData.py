#This is a function to get map data for every state
from subprocess import run
import wget
import os
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', help='output directory', default=os.getcwd())
    args = parser.parse_args()
    
    path = args.outdir

    allStates = ["alabama","arizona","arkansas","california","colorado","connecticut","delaware",
                 "district-of-columbia","florida","georgia","idaho","illinois","indiana","iowa",
                 "kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan","minnesota",
                 "mississippi","missouri","montana","nebraska","nevada","new-hampshire","new-jersey","new-mexico",
                 "new-york","north-carolina","north-dakota","ohio","oklahoma","oregon","pennsylvania",
                 "rhode-island","south-carolina","south-dakota","tennessee","texas",
                 "utah","vermont","virginia","washington","west-virginia","wisconsin","wyoming"]

    allStates = ["rhode-island"]

    link = "https://download.geofabrik.de/north-america/us/"

    for state in allStates:
        stateLink = link + state + "-latest.osm.bz2"
        filePath = os.path.join(path, state + "-latest.osm.bz2")

        if not os.path.exists(filePath):
            wget.download(stateLink,filePath)

        if not os.path.exists(filePath[:-4]):
            run(f'bunzip2 {filePath}')

if __name__ == '__main__':
    main()
