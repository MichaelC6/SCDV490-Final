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

    lat1 = lat1 * np.pi/180
    lat2 = lat2 * np.pi/180
    lon1 = lon1 * np.pi/180
    lon2 = lon2 * np.pi/180
    
    d = np.arccos(np.sin(lat1)*np.sin(lat2) + np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2))
    return d*3958.8 # convert to miles (https://solarsystem.nasa.gov/planets/earth/by-the-numbers/)

def coordFromRadialDist(lat1, lon1, d, lat2=None, lon2=None):
    '''
    calculates the new coordinate

    adapted from: https://www.usgs.gov/faqs/how-much-distance-does-a-degree-minute-and-second-cover-your-maps#:~:text=One%20degree%20of%20latitude%20equals,one%20second%20equals%2080%20feet.

    if lat2 is provided, new longitude is calculated, if lon2 is provided, new latitude is calculated
    '''

    if lat2 is None and lon2 is not None:
        new = lat1 + (d*(1/69))
    elif lat2 is not None and lon2 is None:
        new = lon1 + (d*(1/54.6))
    else:
        raise IOError('Please input either a lat2 or lon2')

    return new
        
