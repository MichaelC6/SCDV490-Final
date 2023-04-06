'''
Functions for analyzing the map data once it is parsed
'''
import numpy as np

def geodesicDist(lat1, lon1, lat2, lon2):
    '''
    calculates the geodesic distance
    
    lat1 [float] : first coordinate latitude
    lon1 [float] : first coordinate longitude
    lat2 [float] : second coordinate latitude
    lon2 [float] : second coordinate longitude

    Returns the distance between the two coordinates in miles
    '''

    # formula from: http://edwilliams.org/avform147.htm#Intro
    # d=acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon1-lon2))

    d = np.arccos(np.sin(lat1)*np.sin(lat2) + np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2))
    return d
