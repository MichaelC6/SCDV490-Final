'''
Class to hold software for the search algorithm. First attempt is DFS
'''
from util.preProcessing import readXML

class Search():

    def __init__(self, filepath):
        '''
        filepath [str] : path to XML file to parse
        '''

        self.filepath = filepath

        # read in the file with our XML parsing code
        self.data = readXML(self.filepath)

        
        
        
