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
    mostFrequentWord = {}
    with open(paramFileNameLex, 'r') as paramFileLex:
        for line in paramFileLex:
            segment, tag = line.strip().split('\t')     
            mostFrequentWord[segment] = tag
            
    with open('../exps/test.tagged', 'w+') as taggedFile, open(testFileName, 'r') as testFile:
        for line in testFile:
            segment = line.strip()        
            if segment == '':
                taggedFile.write('\n')
            else:
                tag = mostFrequentWord.get(segment)
                if tag == None:
                    tag = 'NNP'
                taggedFile.write('{}\t{}\n'.format(segment, tag))
                    
elif model == '2':
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
    
    with open('../exps/test.tagged', 'w+') as taggedFile, open(testFileName, 'r') as testFile:
        sentence = []
        for line in testFile:
            segment = line.strip()
            if segment != '':
                sentence.append(segment)
            else:
                tags = utils.viterbi(sentence, states, emissionProbabilityDict, transitionProbabilityDict)
                for segment, tag in zip(sentence, tags):
                    taggedFile.write('{}\t{}\n'.format(segment, tag))
                taggedFile.write('\n')
                sentence = []

    
