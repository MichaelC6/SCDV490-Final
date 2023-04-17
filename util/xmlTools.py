from classes.tag import Tag
import re

#This is a quick function to append a multi-output function
#To different lists at once
def nAppend(lists,values):
    for list,value in zip(lists,values):
        list.append(value)

#This funtion just splits a regular node line and gets all the necessary information from it.
def readNode(line):
    #The lines are split by spaces, so we need to split by spaces
    line = line.split(" ")
    #Just gets the information from the different parts of the line
    id = int(line[3][4:-1])
    lat = float(line[6][5:-1])
    long = float(line[7][5:-4])
    return id, lat, long

#This function reads a single tag line.
#This is meant to be combined with readAllTags to accomplish its function
def readTag(line):
    #This splits the line by '" ' to account for values with spaces in it
    line = line.split("\" ")

    #Take the key part and split again, taking the 2nd part of it
    key_part = line[0]
    key = key_part.split("k=\"")[1]

    #If gnis is included we need to get rid of it
    if 'gnis' in key:
        key = key.split('gnis')[1][1:]

    #Taking the value part, splitting it again, taking the 2nd part through the last 4 characters.
    value_part = line[1]

    try:
        value = value_part.split("v=\"")[1][:-4]
    except IndexError:
        value = ""
    
    return key, value

#This goes in tandem with readTags so that it can do multiple lines
def readAllTags(file,index):
    #Makes the two empty lists
    keys = []
    values = []
    tagsDone = False
    #While there is still lines to process afterwards...
    while index+1 < len(file) and not tagsDone:

        #If the next line is </node> run this and break
        if '</node>' in file[index + 1]:
            #print(file[index])
            nAppend([keys,values],readTag(file[index]))
            index += 1
            tagsDone = True

        #Otherwise just keep running and return a list
        else:
            nAppend([keys,values],readTag(file[index]))
            index += 1
    return keys,values,index

#This function gets the type of line
#Returns node, tag, way, end of tag, relation
def getType(line):
    #Uses a simple amount of regular expression to try to fill these two lists
    endType = re.findall("</[A-Za-z0-9]+>",line)
    begType = re.findall("<[A-Za-z0-9]+ ",line)

    #If there is a match in the beginning
    if len(begType) > 0:
        #Return the good part
        return begType[0][1:-1]
    
    #If there is not a match in the beginning but end
    elif len(endType) > 0:
        #Return end of with it
        return "end of " + endType[0][2:-1]
    
    #If nothing else, just return None because it's about identification
    else:
        return None
    