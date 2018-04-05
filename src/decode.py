import sys  # This library is imported in order to access the program arguments

if len(sys.argv) < 4:
    print('Incorrect number of arguments')
    print('Correct calling format is: ./decode < model > < heb-pos.test > < param-file1 > [< param-file2 >]')
    exit(0)

model = sys.argv[1]
testFileName = sys.argv[2]
paramFileName1 = sys.argv[3]

segmentMajorityTagDict = {}

with open(paramFileName1, 'r') as paramFile1:
    for line in paramFile1:
        splitLine = line.strip().split('\t')
        seg = splitLine[0]
        posProbs = splitLine[1:]
        maxPos = ''
        maxProb = float('-inf')
        i = 0
        while i < len(posProbs):
            if float(posProbs[i + 1]) > maxProb:
                maxPos = posProbs[i]
                maxProb = float(posProbs[i + 1])
            i += 2
        segmentMajorityTagDict[seg] = maxPos

with open('../exps/test.tagged', 'w') as taggedFile, open(testFileName, 'r') as testFile:
    for line in testFile:
        segment = line.strip()
        tag = segmentMajorityTagDict.get(segment, 'NPP')
        if segment == '':
            taggedFile.write('\n')
        else:
            taggedFile.write('{}\t{}\n'.format(segment, tag))
