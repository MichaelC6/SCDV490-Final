from util.preProcessing import readXML
import os
import pandas as pd

dir = os.getcwd()

testFile = os.path.join(dir,'sampleData','test.xml')


print("We are here!")
df = readXML(testFile)

print("This has finished running!")