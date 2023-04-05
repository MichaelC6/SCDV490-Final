#This is the tag class for organizing tags in the XML file read in
class Tag:
    def __init__(self, keys, values):
        self.keys = keys
        self.values = values
    #This function returns the keys of a function
    def getKeys():
        return keys
    
    #This funtion returns the values of a function
    def getValues():
        return values
    
    #This function gets the number of keys and values
    def getNumKey():
        return len(keys)
    
    #This returns the pair of key and value for a given index
    def getPair(index):
        return keys[index],values[index]
    
    #This gets the value by index
    def getValueByIndex(index):
        return values[index]
    
    #This gets the key by index
    def getKeyByIndex(index):
        return keys[index]
    
    #This gets the value by key
    def getValueByKey(keyName):
        return values[keys.index(keyName)]
    
    #This gets the key by value
    def getKeyByValue(valueName):
        return keys[values.index(valueName)]  
    
    #This is a function to see if this is just an empty object
    def isEmpty():
        return len(keys) == 0