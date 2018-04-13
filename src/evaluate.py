# -*- coding: cp1255 -*-
import sys  # This library is imported in order to access the program arguments

if len(sys.argv) != 5:
    raise ValueError('Incorrect number of arguments \nCorrect calling format is: ./evaluate < *.tagged > < heb-pos.gold > < model > < smoothing(y/n) >')

taggedFileName = sys.argv[1]
goldFileName = sys.argv[2]
model = sys.argv[3]
smoothing = sys.argv[4]

if smoothing == 'y':
    smoothing = True
elif smoothing == 'n':
    smoothing = False
else:
    raise ValueError('Incorrect number of arguments \nCorrect calling format is: ./evaluate < *.tagged > < heb-pos.gold > < model > < smoothing(y/n) >')
with open(taggedFileName, 'r') as taggedFile, open(goldFileName, 'r') as goldFile, open('../exps/test.eval',
                                                                                        'w+') as evalFile:
    correctCount = 0
    totalSentenceLengths = 0
    totalAccuracy = 0

    nj = 0
    N = 0
    A = 0
    
    tagTypeCounter = 0
    tagTypeDict = {}
    tagTypeDictInverse = {}
    confusionMatrix = list()

    for taggedLine in taggedFile:
        goldLine = goldFile.readline().strip()
        if goldLine == '':
            N += 1
            if nj == 0:
                raise ValueError('An error occurred, exiting')
            segAccuracy = correctCount / float(nj)
            if segAccuracy == 1:
                sentAccuracy = 1
            else:
                sentAccuracy = 0
            A += correctCount
            totalSentenceLengths += nj
            totalAccuracy += sentAccuracy
            evalFile.write(str(N) + '\t' + str(segAccuracy) + '\t' + str(sentAccuracy) + '\n')
            correctCount = 0
            nj = 0
        else:
            nj += 1
            goldSegment, goldTag = goldLine.split('\t')
            taggedSegment, taggedTag = taggedLine.strip().split('\t')
            
            newTag = False
            if tagTypeDict.get(goldTag) == None:
                tagTypeDict[goldTag] = tagTypeCounter
                tagTypeDictInverse[tagTypeCounter] = goldTag
                newTag = True                
                
            if tagTypeDict.get(taggedTag) == None:
                tagTypeDict[taggedTag] = tagTypeCounter
                tagTypeDictInverse[tagTypeCounter] = taggedTag
                newTag = True
                
            if newTag:
                for lst in confusionMatrix:
                    lst.append(0)
                tagTypeCounter += 1
                confusionMatrix.append([0 for x in range(tagTypeCounter)])
                
            confusionMatrix[tagTypeDict[taggedTag]][tagTypeDict[goldTag]] += 1
            
            if taggedSegment != goldSegment:
                raise ValueError('An error occurred, exiting')
            if goldTag == taggedTag:
                correctCount += 1

    A = A / float(totalSentenceLengths)
    totalAccuracy = totalAccuracy / float(N)
    evalFile.write('#\n')
    evalFile.write('macro-avg\t{}\t{}\n'.format(A, totalAccuracy))
    print('macro-avg\t{}\t{}\n'.format(A, totalAccuracy))
    
    with open('../exps/confusion.matrix', 'w+') as confusionMatrixFile:
        for i in range(len(confusionMatrix)):
            confusionMatrixFile.write(' '.join(map(lambda x: '%4s' % x, confusionMatrix[i])) + '\n')
        
    maxVal1 = (-1, -1, -1)
    maxVal2 = (-1, -1, -1)
    maxVal3 = (-1, -1, -1)
    for i in range(len(confusionMatrix)):
        for j in range(len(confusionMatrix[i])):
            if i != j:
                if confusionMatrix[i][j] > maxVal3[0]:
                    if confusionMatrix[i][j] > maxVal2[0]:
                        if confusionMatrix[i][j] > maxVal1[0]:
                            maxVal3 = maxVal2
                            maxVal2 = maxVal1
                            maxVal1 = (confusionMatrix[i][j], i, j)
                        else:
                            maxVal3 = maxVal2
                            maxVal2 = (confusionMatrix[i][j], i, j)
                    else:
                        maxVal3 = (confusionMatrix[i][j], i, j)
    
    print('The three most common errors were: ')
    print('{} times {} was tagged as {}'.format(maxVal1[0], tagTypeDictInverse[maxVal1[2]], tagTypeDictInverse[maxVal1[1]]))
    print('{} times {} was tagged as {}'.format(maxVal2[0], tagTypeDictInverse[maxVal2[2]], tagTypeDictInverse[maxVal2[1]]))
    print('{} times {} was tagged as {}'.format(maxVal3[0], tagTypeDictInverse[maxVal3[2]], tagTypeDictInverse[maxVal3[1]]))
            