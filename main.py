import numpy as np
import csv



alphabetDict = {
	'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
	'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25
	}

convertDict = {
    0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i', 9:'j', 10:'k', 11:'l', 12:'m', 13:'n'
    , 14:'o', 15:'p', 16:'q', 17:'r', 18:'s', 19:'t', 20:'u', 21:'v', 22:'w', 23:'x', 24:'y', 25:'z'
}

testSize = 5
wordSize = 1
alphabetSize = 26
testCounter = 0
#first column is label , second column is data
testData = np.zeros([testSize,2])

testWords = []
testLabels = []

trainFirstWord = []
trainSecondWord = []

# dokumandaki '..',  '_ _' olarak degistirildi


def viterbi(query, firstStateProbabilitiy,transitionProbability,emissionProbability):
    sigmaMtr = np.zeros([query.__len__(), alphabetSize])
    for i in range(0, len(firstStateProbabilitiy)):
        plc = alphabetDict[query[0]]
        sigmaMtr[0][i] = firstStateProbabilitiy[i] * emissionProbability[plc][i]

    for i in range(1, query.__len__()):
        for j in range (0, alphabetSize):
            maxValue = 0
            for k in range(0, alphabetSize):
                tmp = sigmaMtr[i-1][k] * transitionProbability[k][j]
                if tmp > maxValue:
                    maxValue = tmp
            plc = alphabetDict[query[i]]
            sigmaMtr[i][j]  = max * emissionProbability[i][j]
    newWord = ''
    for i in range(0, query.__len__()):
        ind = np.argmax(sigmaMtr[i])
        newWord += convertDict[ind]
    return newWord


with open('short.data') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        if (row[0] == '_' and row[1] == '_'):
            wordSize += 1
f.close()
print wordSize

tmpTrWord = ''
tmpFlWord = ''

with open('short.data') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        if (testCounter < testSize) :
            if (row[0] != '_' and row[1] != '_'):
            ## taking first 20k words as TEST
                #testData[testCounter][0] = alphabetDict[row[0]]
                #testData[testCounter][1] = alphabetDict[row[1]]
                tmpTrWord += row[0]
                tmpFlWord += row[1]
            else:
                testCounter += 1
                testWords.append(tmpFlWord)
                testLabels.append(tmpTrWord)
                tmpTrWord = ''
                tmpFlWord = ''
        else:
            if (row[0] != '_' and row[1] != '_'):
            ## taking remaining words as TRAIN
                tmpTrWord += row[0]
                tmpFlWord += row[1]
            else:
                trainFirstWord.append(tmpTrWord)
                trainSecondWord.append(tmpFlWord)
                tmpTrWord = ''
                tmpFlWord = ''
#last word is also added
trainFirstWord.append(tmpTrWord)
trainSecondWord.append(tmpFlWord)
f.close()

#data is taken, building matricecs
trainSize = trainFirstWord.__len__()
firstStateProbabilitiy = np.zeros([alphabetSize, 1])
transitionProbability = np.zeros([alphabetSize, alphabetSize])
emissionProbability = np.zeros(([alphabetSize, alphabetSize]))


for word in trainFirstWord:
    firstStateProbabilitiy[alphabetDict[word[0]]] += 1
    for i in range(0, (word.__len__() - 1 )):
        first = alphabetDict[word[i]]
        second = alphabetDict[word[i+1]]
        transitionProbability[first][second] += 1

for i in range(0,trainSize):
    firstWord = trainFirstWord[i]
    secondWord = trainSecondWord[i]
    for j in range(0,firstWord.__len__()):
        if(firstWord[j] != secondWord[j]):
            first = alphabetDict[firstWord[j]]
            second = alphabetDict[secondWord[j]]
            emissionProbability[first][second] += 1

for i in range(0, alphabetSize):
    totTran = np.sum(transitionProbability[i])
    if totTran != 0:
        for j in range(0, alphabetSize):
            transitionProbability[i][j] = transitionProbability[i][j] / totTran
    totEm = np.sum(emissionProbability[i])
    if totEm != 0:
        for j in range(0, alphabetSize):
            emissionProbability[i][j] = emissionProbability[i][j] / totEm

for word in testWords:
    new = viterbi(word,firstStateProbabilitiy,transitionProbability,emissionProbability)
    print word
    print new
