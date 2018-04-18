import utils
import sys  # This library is imported in order to access the program arguments

if len(sys.argv) != 4:
    raise ValueError('Incorrect number of arguments \nCorrect calling format is: ./train < model > < heb-pos.train > < smoothing(y/n) >')
model = sys.argv[1]
trainFileName = sys.argv[2]
smoothing = sys.argv[3]

if smoothing == 'y':
    smoothing = True
elif smoothing == 'n':
    smoothing = False
else:
    raise ValueError('Incorrect number of arguments \nCorrect calling format is: ./train < model > < heb-pos.train > < smoothing(y/n) >')

trainSegmentTagsDict, unigramDict, bigramDict, unigramCount = utils.analyzeFileFull(trainFileName)
#transitionProbabilitySmoothingNormalizationFactor = 2000


# For model 1 (majority vote tagger) we create a file of the format 
# Si \t Ti - where Si is a segment and Ti is its most common tag
if model == '1':
    with open('../exps/q2.lex', 'w+') as f:
        for segment, tagsDict in trainSegmentTagsDict.items():
            maxTag = ''
            maxCount = 0
            for tag, count in tagsDict.items():
                if count >= maxCount:
                    maxTag = tag
                    maxCount = count
            f.write('{}\t{}\n'.format(segment, maxTag))
            
            
if model == '2':   
    # Create the .lex file as defined in the specifications
    with open('../exps/q3.lex', 'w+') as f:
        unkDict = {}
        for segment, tagsDict in trainSegmentTagsDict.items():
            row = segment
            totalAppearances = 0
            lastTag = ''
            lastCount = 0
            for tag, count in tagsDict.items():
                totalAppearances += count
                lastTag = tag
                lastCount = count
                row += '\t{}\t{}'.format(tag, utils.transformProbability(count / float(unigramDict[tag])))
            if smoothing and totalAppearances == 1:
                # If smoothing is set, then every segment appearing once will
                # add 1 to the appearance of the segment UNK with the same tag
                unkDict[lastTag] = unkDict.get(lastTag, 0) + 1
                # The probability of this emission is divided by 2 for the
                # smoothing. The remaining probability will go to UNK
                f.write('{}\t{}\t{}\n'.format(segment, lastTag, utils.transformProbability(lastCount / float(2 * unigramDict[lastTag]))))
            else:
                f.write(row + '\n')
        if smoothing:
            # If we're smoothing, then we add a UNK row with all the tags
            # that we've added to the unkDict before
            row = 'UNK'
            for tag, count in unkDict.items():
                row += '\t{}\t{}'.format(tag, utils.transformProbability(count / float(2 * unigramDict[tag])))
            f.write('{}\n'.format(row))
    
    singleAppearancesTagDict = {}
    # Counting the number of times tag1 was followed by tag2 only once
    singleAppearances = 0
    for key, value in bigramDict.items(): 
        if value == 1:
            singleAppearances += 1
            tag = key.split(',')[1]
            singleAppearancesTagDict[tag] = singleAppearancesTagDict.get(tag, 0) + 1

    # Create the .gram file as defined in the specifications
    with open('../exps/q3.gram', 'w+') as f:
        f.write('\\data\\\n')
        f.write('ngram 1 = {}\n'.format(len(unigramDict)))
        f.write('ngram 2 = {}\n'.format(len(bigramDict)))
        f.write('\n')
        f.write('\\1-grams\\\n')
        # Add all the 1-gram rows using unigramDict
        for key, value in unigramDict.items():
            f.write('{}\t{}\n'.format(utils.transformProbability(value / float(unigramCount)), key))
        f.write('\n')
        f.write('\\2-grams\\\n')
        # Add all the 1-gram rows using unigramDict
        for key, value in bigramDict.items():
#            if smoothing and value == 1:
#                f.write('{}\tUNK\t{}\n'.format(utils.transformProbability(value / float(singleAppearances)), key.split(',')[1]))
            f.write('{}\t{}\n'.format(utils.transformProbability(value / float(unigramDict[key.split(',')[0]])), '\t'.join(key.split(','))))
        if smoothing:
            for key, value in singleAppearancesTagDict.items():
                f.write('{}\tUNK\t{}\n'.format(utils.transformProbability(value / float(singleAppearances)), key))
        f.write('\n')
        