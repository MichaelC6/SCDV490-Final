#!/bin/bash

# download all the data
python3 util/getAllData.py --outdir data

# convert all OSM files to json
python3 util/getJSONs.py --allStates

# generate charging network files
python3 util/getChargingNetwork.py
