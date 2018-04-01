import utils
import sys  # This library is imported in order to access the program arguments

if len(sys.argv) < 4:
    print 'Incorrect number of arguments'
    print 'Correct calling format is: ./decode < model > < heb-pos.test > < param-file1 > [< param-file2 >]'
    exit(0)

model = sys.argv[1]
testFileName = sys.argv[2]
paramFileName1 = sys.argv[3]


paramFile1 = open(paramFileName1, 'r')
segmentMajorityTagDict = {}


for line in paramFile1:
    splitLine = line.strip().split('\t')
    seg = splitLine[0]
    posProbs = splitLine[1:]
    maxPos = ''
    maxProb = 0
    i = 0
    while i < len(posProbs):
        if posProbs[i + 1] > maxProb:
            maxPos = posProbs[i]
            maxProb = posProbs[i + 1]
        i += 2
    segmentMajorityTagDict[seg] = maxPos
    
paramFile1.close()

testFile = open(testFileName, 'r')
taggedFile = open('../exps/test.tagged','w')

for line in testFile:
    segment = line.strip()
    tag = segmentMajorityTagDict.get(segment, 'NPP')
    if segment == '':
        taggedFile.write('\n')
    else:
        taggedFile.write(segment + '\t' + tag + '\n')

testFile.close()
taggedFile.close()
