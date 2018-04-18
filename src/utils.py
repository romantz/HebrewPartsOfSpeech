# -*- coding: utf_8 -*-
import math

signLookup = {'yyCM': ',', 'yyCLN': ':', 'yyLRB': '(', 'yyQUOT': '\"', 'yyDOT': '.', 'yyDASH': '-',
              'yyRRB': ')', 'yyEXCL': '!', 'yyQM': '?', 'yySCLN': ';', 'yyELPS': '...'}

letterLookup = {'A': 'א', 'B': 'ב', 'G': 'ג', 'D': 'ד', 'H': 'ה', 'V': 'ו', 'W': 'ו', 'Z': 'ז', 'U': '\"',
                'X': 'ח', 'T': 'ת', 'I': 'י', 'K': 'כ', 'L': 'ל', 'M': 'מ', 'N': 'נ', 'O': '%', 'J': 'ט',
                'S': 'ס', 'E': 'ע', 'P': 'פ', 'C': 'צ', 'Q': 'ק', 'R': 'ר', 'F': 'ש'}

# The probability format. True for logprob and False for regular probability
logprob = True

def diminishProbability(transitionProb):
    """
    This function is used to diminish emission or transition probability
    for a smoothed (UNK) value in order to ensure that if the value exists,
    it would always be preferred over the smoothed value
    
    The value of dimValue has been derived empirically 
    """
    dimValue = 500
    if logprob:
        return transitionProb - math.log(dimValue)
    else:
        return transitionProb / float(dimValue)

def nullProbability():
    """
    Get the null probability which is 0 for regular and negative 
    infinity for logprob
    """
    if logprob:
        return float('-inf')
    else:
        return 0
    
def aggregateProbabilities(p1, p2):
    """
    Get the probability aggregation function which is multiplication 
    for regular and addition logprob
    """
    if logprob:
        return p1 + p2
    else:
        return p1 * p2

def transformProbability(p):
    """
    Transform given probability to logprob
    """
    if logprob:
        return math.log(p)
    else:
        return p

def decode(word):
    """
    A function for debugging - receives a word and decodes it to Hebrew letters
    """
    for sign, letter in signLookup.items():
        word = word.replace(sign, letter)
    for sign, letter in letterLookup.items():
        word = word.replace(sign, letter)
    return word


def analyzeFileQ1(fileName):
    """
    File analysis for Q1
    
    Input:
        A file name of a tagged file
    
    Returns:
        segmentTagsDict - A dictionary which maps a word to a dictionary
                          which maps the given word's tag with the number 
                          of times the word appeared with that tag
        segmentTagPairs - A set which holds all the segment, tag pairs that
                          appeared in the given file
        segmentCount -    Total number of unigrams in the file
    """
    segmentTagPairs = set()
    segmentTagsDict = {}
    segmentCount = 0

    with open(fileName, 'r') as f:
        for line in f:
            line = line.strip()
            if line != '':
                segmentCount += 1
                segment, tag = line.split('\t')
                segmentTagPairs.add((segment, tag))
                entryValue = segmentTagsDict.get(segment)
                if entryValue == None:
                    # The given semgment was not yet observed in the input file
                    # so we add it to the dict with its current tag
                    segmentTagsDict[segment] = {tag: 1}
                else:
                    # The given segment was observed in the given file
                    # we update the current tag count for this segment by +1
                    segmentTagsDict[segment][tag] = entryValue.get(tag, 0) + 1
    return segmentTagsDict, segmentTagPairs, segmentCount


def analyzeFileFull(fileName):
    """
    File analysis for Q2 and Q3
    
    Input:
        A file name of a tagged file
    
    Returns:
        segmentTagsDict - A dictionary which maps a word to a dictionary
                          which maps the given word's tag with the number 
                          of times the word appeared with that tag
        unigramDict -     A dictionary which maps a tag in the corpus to the 
                          number of times this tag appeared in the input file
        bigramDict -      A dictionary which maps a tag,tag pair to the number
                          of times this tags were seen in this immediate order
                          in the input file
        unigramCount -    Total number of unigrams appearing in the input file
                          (including <S> and <E> signs)
    """
    segmentTagsDict = {}
    unigramDict = {}
    bigramDict = {}
    unigramCount = 0
    lastTag = '<S>'
    unigramDict[lastTag] = 0
    newLine = True

    with open(fileName, 'r') as f:
        for line in f:
            line = line.strip()
            if line != '':
                # Non empty line is a word in a sentence
                unigramCount += 1
                segment, tag = line.split('\t')
                entryValue = segmentTagsDict.get(segment)
                if entryValue == None:
                    # The given semgment was not yet observed in the input file
                    # so we add it to the dict with its current tag
                    segmentTagsDict[segment] = {tag: 1}
                else:
                    # The given segment was observed in the given file
                    # we update the current tag count for this segment by +1
                    segmentTagsDict[segment][tag] = entryValue.get(tag, 0) + 1
                # Count the current tag in the unigramDict
                unigramDict[tag] = unigramDict.get(tag, 0) + 1
                # Count the current and the last tag in the bigramDict
                bigramDict[lastTag + ',' + tag] = bigramDict.get(lastTag + ',' + tag, 0) + 1
                lastTag = tag
                if newLine == True:
                    # If it's a new line we add +1 to the number of
                    # appearances of <S> in the unigramDict
                    unigramDict['<S>'] = unigramDict.get('<S>', 0) + 1
                    newLine = False
                
            else:
                # An empty line indicates the end of a sentence
                # counting <S> and <E> for current sentence
                unigramCount += 2
                # Add +1 to the number of appearances of <E> in the unigramDict
                unigramDict['<E>'] = unigramDict.get('<E>', 0) + 1
                # Add +1 to the number of appearances of the last word in the
                # sentence followed by <E>
                bigramDict[lastTag + ',<E>'] = bigramDict.get(lastTag + ',<E>', 0) + 1
                lastTag = '<S>'
                # Indicate that this is a new line for the next iteration
                newLine = True
    return segmentTagsDict, unigramDict, bigramDict, unigramCount


def viterbi(sentence, states, emissionProbabilityDict, transitionProbabilityDict):
    """
    An implementation of the Viterbi algorithm
    
    Input:
        sentence - A list of words representing a sentence
        states - Aset of all the possible tags in the corpus
        emissionProbabilityDict - A dictionary which maps a word to a dictionary 
                                  which maps a tag to the probability that the
                                  given word is emitted by this tag: P(Wi | Ti)
        transitionProbabilityDict - A dictionary which maps tag 1 to a dictionry
                                    which maps tag 2 to the probability that
                                    tag 1 transitions to tag 2: P(T2 | T1)
                                    
    Returns:
        A list of tags for the given sentence
    """
    # A list of dictionaries. Element i in the list is a dictionary which 
    # corresponds to the i'th word in the sentence. Each dictioney maps a
    # state (tag) to a tuple (prob, state) where prob is the highest probability
    # to achieve the given tag and state is the previous tag which gives this 
    # probability (this is used for backtracking)
    v = [{}]
    
    # The best tags found fot the given sentence
    tags = []
    
    for state in states:
        # The transition probability of the first iteration is P(state | <S>)
        transitionProb = transitionProbabilityDict.get('<S>', {}).get(state)
        if transitionProb == None:
            # If the given transition probability was not found we look for
            # the probability of P(state | UNK) in case smoothing used in 
            # training. If such probability doesn't exist, return null probability
            transitionProb = diminishProbability(transitionProbabilityDict.get('UNK', {}).get(state, nullProbability()))
            
        # The emission probability of the first iteration is P(W1 | state)
        # if the given segment was not found, we look for the probability 
        # of P(UNK | state)
        emissionProb = emissionProbabilityDict.get(sentence[0])
        if emissionProb != None:
            emissionProb = emissionProb.get(state, nullProbability())
        else:
            emissionProb = diminishProbability(emissionProbabilityDict.get('UNK', {}).get(state, nullProbability()))
            
        # The 0 element of v with the current state is the aggregation 
        # of the emissions and transition probabilities
        v[0][state] = aggregateProbabilities(transitionProb, emissionProb), ''
    for i in range(1, len(sentence)):
        v.append({})
        for state1 in states:
            maxProb = nullProbability()
            maxState = ''
            
            # Calculate the emission probability for state1
            if emissionProbabilityDict.get(sentence[i]) != None:
                emissionProb = emissionProbabilityDict[sentence[i]].get(state1, nullProbability())
            else:
                emissionProb = diminishProbability(emissionProbabilityDict.get('UNK', {}).get(state1, nullProbability()))
            
            # calculate every possible transition probability and take the max
            for state2 in states:
                transitionProb = transitionProbabilityDict.get(state2, {}).get(state1)
                if transitionProb == None:
                    transitionProb = diminishProbability(transitionProbabilityDict.get('UNK', {}).get(state1, nullProbability()))
                    
                # Current probability is the aggregation between emission,
                # transition and the previous value of v for state2
                currentProb = aggregateProbabilities(aggregateProbabilities(v[i - 1][state2][0], transitionProb), emissionProb)
                if currentProb >= maxProb:
                    maxState = state2
                    maxProb = currentProb
            # Now we have the maximum probability for the given state and
            # the previous state that gave this probability
            v[i][state1] = maxProb, maxState
    overallMaxProb = nullProbability()
    overallMaxState = ''
    
    # Look for a non null probability entry in v starting from the last
    # element and going in reverse
    for i in reversed(range(len(v))):
        for tag, (prob, prevTag) in v[i].items():
            if prob >= overallMaxProb:
                overallMaxProb = prob
                overallMaxState = tag
        # If no probability different than null was found for the current
        # iteration, tag the current word as NNP
        if overallMaxProb == nullProbability():
            tags.append('NNP')
        else:
            break
    # If a non null probability was found, start backtracking until all the
    # words are tagged
    if i >= 0:
        tags.append(overallMaxState)
        lastTag = overallMaxState
        while i >= 0:
            newTag = v[i][lastTag][1]
            if newTag != '':
                tags.append(newTag)
            lastTag = newTag
            i -= 1
    return list(reversed(tags))
    