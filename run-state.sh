#!/bin/bash

# download all the data
echo 'Downloading the data..'
python3 util/getAllData.py --outdir data/osm --state $1

# convert all OSM files to json
echo 'Cleaning downloaded data...'
python3 util/getJSONs.py --filename $1-latest.osm

# generate charging network files
echo 'Generating the charging network...'
python3 util/getChargingNetwork.py --infile data/jsons/$1-latest.json

# generate all the analysis plots
echo 'Making the analysis plots...'
python3 util/makePlots.py
