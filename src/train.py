import utils
import sys  # This library is imported in order to access the program arguments

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

trainSegmentTagsDict, unigramDict, bigramDict, unigramCount = utils.analyzeFileQ2(trainFileName)

if model == '1':
    with open('../exps/param.lex', 'w+') as f:
        for segment, tagsDict in trainSegmentTagsDict.items():
            maxTag = ''
            maxCount = 0
            for tag, count in tagsDict.items():
                if count >= maxCount:
                    maxTag = tag
                    maxCount = count
            f.write(segment + '\t' + maxTag + '\n')
            
if model == '2':   
    
    with open('../exps/param.lex', 'w+') as f:
        unkDict = {}
        for segment, tagsDict in trainSegmentTagsDict.items():
            row = segment
            totalAppearances = 0
            lastTag = ''
            for tag, count in tagsDict.items():
                totalAppearances += count
                lastTag = tag
                row += '\t' + tag + '\t' + str(utils.transformProbability(count / float(unigramDict[tag])))
            if smoothing and totalAppearances == 1:
                unkDict[lastTag] = unkDict.get(lastTag, 0) + 1
            else:
                f.write(row + '\n')
        if smoothing:
            row = 'UNK'
            for tag, count in unkDict.items():
                row += '\t' + tag + '\t' + str(utils.transformProbability(count / float(unigramDict[tag])))
            f.write(row + '\n')
    
    with open('../exps/param.gram', 'w+') as f:
        f.write('\\data\\\n')
        f.write('ngram 1 = {}\n'.format(len(unigramDict)))
        f.write('ngram 2 = {}\n'.format(len(bigramDict)))
        f.write('\n')
        f.write('\\1-grams\\\n')
        for key, value in unigramDict.items():
            f.write('{}\t{}\n'.format(utils.transformProbability(value / float(unigramCount)), key))
        f.write('\n')
        f.write('\\2-grams\\\n')
        for key, value in bigramDict.items():
            f.write('{}\t{}\n'.format(utils.transformProbability(value / float(unigramDict[key.split(',')[0]])), '\t'.join(key.split(','))))
        f.write('\n')
        