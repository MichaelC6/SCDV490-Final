'''
This file downloads and formats the data correctly for the rest of the code
for this project
'''

import os
from subprocess import run

# hard code in boundary coordinates for now
llLat = 42.50 # lower left latitude
llLon = -74.00 # lower left longitude
urLat = 42.6#43.0609 # upper right latitude
urLon = -73.9#-73.5396 # upper right longitude

outfile = os.path.join(os.getcwd(),'sampleData/test2.xml')

if not os.path.isfile(outfile):
    # download the data using wget in a subprocess
    #url=f"http://overpass-api.de/api/interpreter?data=(node({llLat},{llLon},{urLat},{urLon});<;rel(br);); meta;"
    url = f'https://api.openstreetmap.org/api/0.6/map?bbox={llLat},{llLon},{urLat},{urLon}'
    cmd = f'wget -O {outfile} "{url}"'
    print(cmd)
    run(cmd, shell=True)
else:
    print('Output XML file already exists, skipping...')
