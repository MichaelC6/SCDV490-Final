'''
This file downloads and formats the data correctly for the rest of the code
for this project
'''

import os
import overpy

# hard code in boundary coordinates for now
llLat = 42.5609 # lower left latitude
llLon = -74.0396 # lower left longitude
urLat = 42.8#43.0609 # upper right latitude
urLon = -73.8#-73.5396 # upper right longitude

outfile = os.path.join(os.getcwd(),'test.xml')

query = f'[out:json];node({llLat},{llLon},{urLat},{urLon});out;'

api = overpy.Overpass()
result = api.query(query)
print(result)
