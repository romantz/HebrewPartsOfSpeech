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
    
if model == '1':
    evalFileName = '../results/q2.eval'
    confusionMatrixFileName = '../exps/q2-confusion.matrix'
else:
    evalFileName = '../results/q3.eval'
    confusionMatrixFileName = '../exps/q3-confusion.matrix'
    
with open(taggedFileName, 'r') as (taggedFile
     ), open(goldFileName, 'r') as (goldFile
     ), open(evalFileName, 'w+') as evalFile:
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
    
    evalFile.write('#-------------------------------------\n')
    evalFile.write('#  Part-of-Speech Tagging Evaluation\n')
    evalFile.write('#-------------------------------------\n')
    evalFile.write('#\n')
    evalFile.write('#  Model: ' + str(model) + '\n')
    evalFile.write('#  Smoothing: ' + str(smoothing) + '\n')
    evalFile.write('#  Test File: ' + taggedFileName + '\n')
    evalFile.write('#  Gold File: ' + goldFileName + '\n')
    evalFile.write('#\n')
    evalFile.write('#-------------------------------------\n')
    evalFile.write('# sent-num word-accuracy sent-accuracy\n')
    evalFile.write('#-------------------------------------\n')                   

                       
    # Go over the tagged and gold file line by line
    for taggedLine in taggedFile:
        goldLine = goldFile.readline().strip()
        if goldLine == '':
            # We've finished reading a sentence
            N += 1
            if nj == 0:
                # Empty sentence has been read, this is an error
                raise ValueError('An error occurred, exiting')
            # Calculate the segment accuracy
            segAccuracy = correctCount / float(nj)
            # Calculate the sentence accuracy
            if segAccuracy == 1:
                sentAccuracy = 1
            else:
                sentAccuracy = 0
            A += correctCount
            totalSentenceLengths += nj
            totalAccuracy += sentAccuracy
            evalFile.write('{}\t{}\t{}\n'.format(N, segAccuracy, sentAccuracy))
            correctCount = 0
            nj = 0
        else:
            # Read a segment and its tag from both tagged and gold files
            nj += 1
            goldSegment, goldTag = goldLine.split('\t')
            taggedSegment, taggedTag = taggedLine.strip().split('\t')
            
            newTag = False
            if tagTypeDict.get(goldTag) == None:
                tagTypeDict[goldTag] = tagTypeCounter
                tagTypeDictInverse[tagTypeCounter] = goldTag
                for lst in confusionMatrix:
                    lst.append(0)
                tagTypeCounter += 1
                confusionMatrix.append([0 for x in range(tagTypeCounter)])
                
            if tagTypeDict.get(taggedTag) == None:
                tagTypeDict[taggedTag] = tagTypeCounter
                tagTypeDictInverse[tagTypeCounter] = taggedTag
                for lst in confusionMatrix:
                    lst.append(0)
                tagTypeCounter += 1
                confusionMatrix.append([0 for x in range(tagTypeCounter)])
            
            # Add the current tagging to the correct place in the confusion
            # matrix
            confusionMatrix[tagTypeDict[taggedTag]][tagTypeDict[goldTag]] += 1
            
            if taggedSegment != goldSegment:
                # If the current segment in the tagged file does not match 
                # the current segment in the gold file that means that an
                # error occurred
                raise ValueError('An error occurred, exiting')
            if goldTag == taggedTag:
                correctCount += 1
    
    A = A / float(totalSentenceLengths)
    totalAccuracy = totalAccuracy / float(N)
    evalFile.write('#-------------------------------------\n')
    evalFile.write('macro-avg\t{}\t{}\n'.format(A, totalAccuracy))
    print('macro-avg\t{}\t{}\n'.format(A, totalAccuracy))
    
    # Output confusion matrix to a file
    with open(confusionMatrixFileName, 'w+') as confusionMatrixFile:
        confusionMatrixFile.write('\t')
        for i in range(tagTypeCounter):
            confusionMatrixFile.write(tagTypeDictInverse[i] + '\t')
        confusionMatrixFile.write('\n')
        for i in range(len(confusionMatrix)):
            confusionMatrixFile.write(tagTypeDictInverse[i] + '\t' + ' '.join(map(lambda x: '%7s' % x, confusionMatrix[i])) + '\n')
        
    # Calculate the 3 most common errors
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
            