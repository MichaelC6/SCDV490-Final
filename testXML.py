from util.preProcessing import readXML,readXMLAsList,readXMLAsDict
import os
import pandas as pd

dir = os.getcwd()

file = 'test.xml'

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


df3 = readXMLAsDict(testFile)

print(df3.head())
#print(dict[0])

print("This has finished running!")
