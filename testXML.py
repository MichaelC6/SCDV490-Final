from util.preProcessing import readXML
import os
import pandas as pd

dir = os.getcwd()

testFile = os.path.join(dir,'sampleData','test2.xml')


print()
print()
print("We are running with 1 multiprocessor!")

df = readXML(testFile, 1)

print("This has finished running!")
print()
print()
print()
print()
print("We are running with 12 multiprocessors!")

df = readXML(testFile, 10)

print("This has finished running!")