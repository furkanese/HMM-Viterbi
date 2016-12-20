import numpy as np
import csv

alphabetDict = {
	'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
	'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25
	}

testSize = 20000
wordSize = 1
testCounter = 0
#first column is label , second column is data
testData = np.zeros([testSize,2])
testWords = []
testLabels = []


with open('docs.data') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        if (row[0] == '_' and row[1] == '_') or (row[0] == '.' and row[1] == '.'):
            wordSize += 1
f.close()
print wordSize

tmpTrWord = ''
tmpFlWord = ''

with open('docs.data') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        if (testCounter < testSize) :
            if (row[0] != '_' and row[1] != '_') and (row[0] != '.' and row[1] != '.'):
                testData[testCounter][0] = alphabetDict[row[0]]
                testData[testCounter][1] = alphabetDict[row[1]]
                tmpTrWord += row[0]
                tmpFlWord += row[1]
            else:
                testCounter += 1
                testWords.append(tmpFlWord)
                testLabels.append(tmpTrWord)
                tmpTrWord = ''
                tmpFlWord = ''
f.close()

for row in testWords:
    print(row)



