import utils
import sys  # This library is imported in order to access the program arguments
import math

if len(sys.argv) != 4:
    print('Incorrect number of arguments')
    print('Correct calling format is: ./train < model > < heb-pos.train > < smoothing(y/n) >')
    exit(0)

model = sys.argv[1]
trainFileName = sys.argv[2]
smoothing = sys.argv[3]

if smoothing == 'y':
    smoothing = True
elif smoothing == 'n':
    smoothing = False
else:
    print('Incorrect calling format')
    print('Correct calling format is: ./train < model > < heb-pos.train > < smoothing(y/n) >')
    exit(0)

trainSegmentTagsDict, unigramDict, bigramDict = utils.analyzeFileQ2(trainFileName)

with open('../exps/param.lex', 'w+') as f:
    if int(model) == 1:
        for segment, tagsDict in trainSegmentTagsDict.items():
            row = segment
            totalSegmentOccurrences = sum(tagsDict.values())
            for tag, count in tagsDict.items():
                row += '\t' + tag + '\t' + str(math.log(count / float(totalSegmentOccurrences)))
            f.write(row + '\n')

with open('../exps/param.gram', 'w+') as f:
    f.write('\\data\\\n')
    f.write('ngram 1 = {}\n'.format(len(unigramDict)))
    f.write('ngram 2 = {}\n'.format(len(bigramDict)))
    f.write('\n')
    f.write('\\1-grams\\\n')
    for key, value in unigramDict.items():
        f.write('{}\t{}\n'.format(value, key))
    f.write('\n')
    f.write('\\2-grams\\\n')
    for key, value in bigramDict.items():
        f.write('{}\t{}\n'.format(value, '\t'.join(key.split(','))))
    f.write('\n')
