from util.preProcessing import readXML
import os
import pandas as pd

dir = os.getcwd()

file = 'new-york-latest.osm'

testFile = os.path.join(dir,'sampleData',file)


# print()
# print()
# print("We are running old version")

# #df = readXML(testFile, 1)

# print(df.head())
# print("This has finished running!")
# print()
# print()
print(f"FILE: {file}")
print()
print("We are running Dictionary version")


table = readXML(testFile)

print(table.info)
#print(dict[0])

print("This has finished running!")
