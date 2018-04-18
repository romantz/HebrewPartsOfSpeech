import utils
import sys  # This library is imported in order to access the program arguments

if len(sys.argv) < 4:
    raise ValueError('Incorrect number of arguments \nCorrect calling format is: ./decode < model > < heb-pos.test > < param-file1 > [< param-file2 >]')

model = sys.argv[1]
testFileName = sys.argv[2]
paramFileNameLex = sys.argv[3]

if model == '2' and len(sys.argv) < 5:
    raise ValueError('Incorrect number of arguments \nCorrect calling format is: ./decode < model > < heb-pos.test > < param-file1 > [< param-file2 >]')
    
if len(sys.argv) == 5:
    paramFileNameGram = sys.argv[4]


if model == '1':
    # If the model is 1, we read the lex file and save for each segment its
    # most frequent tag in the dictionary mostFrequentTag
    mostFrequentTag = {}
    with open(paramFileNameLex, 'r') as paramFileLex:
        for line in paramFileLex:
            segment, tag = line.strip().split('\t')     
            mostFrequentTag[segment] = tag
            
    with open('../results/q2.tagged', 'w+') as taggedFile, open(testFileName, 'r') as testFile:
        for line in testFile:
            segment = line.strip()        
            if segment == '':
                taggedFile.write('\n')
            else:
                # Each segment is tagged with the tag found in the dictionary
                # If no tag has been found, the segment is tagged as NNP
                tag = mostFrequentTag.get(segment)
                if tag == None:
                    tag = 'NNP'
                taggedFile.write('{}\t{}\n'.format(segment, tag))
                    
elif model == '2':
    # For model 2, we read the lex file and create the emissionProbabilityDict
    # This dict maps a segment to a dictionary which maps a tag to the 
    # probability that the segment is emitted by this tag
    emissionProbabilityDict = {}
    with open(paramFileNameLex, 'r') as paramFileLex:
        for line in paramFileLex:
            splitLine = line.strip().split('\t')
            seg = splitLine[0]
            posProbs = splitLine[1:]
            i = 0
            currentSegmentDict = {}
            while i < len(posProbs):
                currentSegmentDict[posProbs[i]] = float(posProbs[i + 1])
                i += 2
            emissionProbabilityDict[seg] = currentSegmentDict
    
    # The transition probabilities are stored in transitionProbabilityDict
    # These probabilities are derived from the .gram file.
    # transitionProbabilityDict maps tag 1 to a dicionary which maps tag 2 to
    # the probability that tag 1 is followed by tag 2
    transitionProbabilityDict = {}
    states = set()
    with open(paramFileNameGram, 'r') as paramFileGram:
        reachedUnigram = False
        reachedBigram = False
        for line in paramFileGram:
            line = line.strip()
            if line == '':
                if reachedUnigram == True:
                    reachedUnigram = False
                if reachedBigram == True:
                    reachedBigram = False
            elif reachedUnigram == False and line == '\\1-grams\\':
                reachedUnigram = True
            elif reachedUnigram == True and line != '':
                _, tag = line.split('\t')
                if tag != '<S>' and tag != '<E>':
                    states.add(tag)
            elif reachedBigram == False and line == '\\2-grams\\':
                reachedBigram = True
            elif reachedBigram == True and line != '':
                prob, tag1, tag2 = line.split('\t')
                if transitionProbabilityDict.get(tag1) == None:
                    transitionProbabilityDict[tag1] = {}
                transitionProbabilityDict[tag1][tag2] = float(prob)
    
    with open('../results/q3.tagged', 'w+') as (taggedFile
        ), open(testFileName, 'r') as testFile:
        sentence = []
        for line in testFile:
            segment = line.strip()
            if segment != '':
                sentence.append(segment)
            else:
                # When we're done reading a sentence, we run the Viterbi
                # algorithm on it to derive its tags
                tags = utils.viterbi(sentence, states, emissionProbabilityDict, transitionProbabilityDict)
                for segment, tag in zip(sentence, tags):
                    taggedFile.write('{}\t{}\n'.format(segment, tag))
                taggedFile.write('\n')
                sentence = []

    
