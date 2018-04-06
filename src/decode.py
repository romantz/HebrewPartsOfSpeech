import sys  # This library is imported in order to access the program arguments

if len(sys.argv) < 4:
    print('Incorrect number of arguments')
    print('Correct calling format is: ./decode < model > < heb-pos.test > < param-file1 > [< param-file2 >]')
    exit(0)

model = sys.argv[1]
testFileName = sys.argv[2]
paramFileNameLex = sys.argv[3]

if len(sys.argv) == 5:
    paramFileNameGram = sys.argv[4]

emitionProbabilityDict = {}

with open(paramFileNameLex, 'r') as paramFileLex:
    for line in paramFileLex:
        splitLine = line.strip().split('\t')
        seg = splitLine[0]
        posProbs = splitLine[1:]
        i = 0
        currentSegmentDict = {}
        while i < len(posProbs):
            currentSegmentDict[posProbs[i]] = posProbs[i + 1]
            i += 2
        emitionProbabilityDict[seg] = currentSegmentDict

if model == '1':
    with open('../exps/test.tagged', 'w+') as taggedFile, open(testFileName, 'r') as testFile:
        for line in testFile:
            segment = line.strip()        
            if segment == '':
                taggedFile.write('\n')
            else:
                tags = emitionProbabilityDict.get(segment)
                if tags != None:
                    maxPos = ''
                    maxProb = float('-inf')
                    for key, value in tags.items():
                        if float(value) > maxProb:
                            maxPos = key
                            maxProb = float(value)
                    tag = maxPos
                else:
                    tag = 'NPP'
                taggedFile.write('{}\t{}\n'.format(segment, tag))
                    
    
