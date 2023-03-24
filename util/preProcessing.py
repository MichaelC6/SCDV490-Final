#These are functions associated with preprocessing data.

import pandas as pd
import xml.etree.ElementTree as ET
import overpy

# This takes in the file path of data and return a dataframe.
def getDataFrame(path):
    return pd.read_csv(path)

def readXML(filepath):
    '''
    Reads an XML file from a Overpass query and outputs an overpy Result object

    filepath [str] : complete path to the XML file
    Returns : overpy.Result object
    '''

    # use the overpass API
    et = ET.parse(filepath)

    # start using overpy
    result = overpy.Result()
    result = result.from_xml(et.getroot(), parser=1)

    return result
    
