'''
This file downloads and formats the data correctly for the rest of the code
for this project
'''

import os
import overpy
from subprocess import run
import pandas as pd

# hard code in boundary coordinates for now
llLat = 42.5609 # lower left latitude
llLon = -74.0396 # lower left longitude
urLat = 43.0609 # upper right latitude
urLon = -73.5396 # upper right longitude

outfile = os.path.join(os.getcwd(),'test.xml')

if not os.path.isfile(outfile):
    # download the data using wget in a subprocess
    url=f"http://overpass-api.de/api/interpreter?data=(node({llLat},{llLon},{urLat},{urLon});<;rel(br););out meta;"
    cmd = f'wget -O {outfile} "{url}"'
    run(cmd, shell=True)

# use the overpass API
df = pd.read_xml(outfile)

# start using overpy
result = overpy.Result().from_xml(df.to_string())
