import utils
import sys  # This library is imported in order to access the program arguments
import math

if len(sys.argv) != 4:
    print 'Incorrect number of arguments'
    print 'Correct calling format is: ./train < model > < heb-pos.train > < smoothing(y/n) >'
    exit(0)

model = sys.argv[1]
trainFileName = sys.argv[2]
smoothing = sys.argv[3]

if smoothing == 'y':
    smoothing = True
elif smoothing == 'n':
    smoothing = False
else:
    print 'Incorrect calling format'
    print 'Correct calling format is: ./train < model > < heb-pos.train > < smoothing(y/n) >'
    exit(0)

trainSegmentTagsDict, _, _, _ = utils.analyzeFile(trainFileName)

f = open('../exps/param.lex','w')

if int(model) == 1:
    for segment, tagsDict in trainSegmentTagsDict.iteritems():
        row = segment
        totalSegmentOccurrences = sum(tagsDict.itervalues())
        for tag, count in tagsDict.iteritems():
            row += '\t' + tag + '\t' + str(math.log(count / float(totalSegmentOccurrences), 10))
        f.write(row + '\n')
        
f.close()
        
