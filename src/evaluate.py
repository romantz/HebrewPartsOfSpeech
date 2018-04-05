# -*- coding: cp1255 -*-
import sys  # This library is imported in order to access the program arguments

if len(sys.argv) != 5:
    print('Incorrect number of arguments')
    print('Correct calling format is: ./evaluate < *.tagged > < heb-pos.gold > < model > < smoothing(y/n) >')
    exit(0)

taggedFileName = sys.argv[1]
goldFileName = sys.argv[2]
model = sys.argv[3]
smoothing = sys.argv[4]

if smoothing == 'y':
    smoothing = True
elif smoothing == 'n':
    smoothing = False
else:
    print('Incorrect calling format')
    print('Correct calling format is: ./evaluate < *.tagged > < heb-pos.gold > < model > < smoothing(y/n) >')
    exit(0)

with open(taggedFileName, 'r') as taggedFile, open(goldFileName, 'r') as goldFile, open('../exps/test.eval',
                                                                                        'w') as evalFile:
    correctCount = 0
    totalSentenceLengths = 0
    totalAccuracy = 0

    nj = 0
    N = 0
    A = 0

    for taggedLine in taggedFile:
        goldLine = goldFile.readline().strip()
        if goldLine == "":
            N += 1
            if nj == 0:
                print('An error occurred, exiting')
                exit(0)
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
            goldSegment, goldTag = goldLine.split("\t")
            taggedSegment, taggedTag = taggedLine.strip().split("\t")
            if taggedSegment != goldSegment:
                print('An error occurred, exiting')
                exit(0)
            if goldTag == taggedTag:
                correctCount += 1

    A = A / float(totalSentenceLengths)
    totalAccuracy = totalAccuracy / float(N)
    evalFile.write('#————————————————————————\n')
    evalFile.write('macro-avg\t' + str(A) + '\t' + str(totalAccuracy) + '\n')
