'''
Functions for analyzing the map data once it is parsed
'''
from geopy.distance import geodesic

def dist(lat1, lon1, lat2, lon2, measure='miles'):
    '''
    Wrapper function for the geopy geodesic distance calculation
    
    lat1 [float] : first coordinate latitude
    lon1 [float] : first coordinate longitude
    lat2 [float] : second coordinate latitude
    lon2 [float] : second coordinate longitude

    Returns the distance between the two coordinates in miles
    '''
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    d = geodesic(coord1, coord2)
    return d.miles
