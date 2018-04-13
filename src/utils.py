# -*- coding: utf_8 -*-
import math

signLookup = {'yyCM': ',', 'yyCLN': ':', 'yyLRB': '(', 'yyQUOT': '\"', 'yyDOT': '.', 'yyDASH': '-',
              'yyRRB': ')', 'yyEXCL': '!', 'yyQM': '?', 'yySCLN': ';', 'yyELPS': '...'}

letterLookup = {'A': 'א', 'B': 'ב', 'G': 'ג', 'D': 'ד', 'H': 'ה', 'V': 'ו', 'W': 'ו', 'Z': 'ז', 'U': '\"',
                'X': 'ח', 'T': 'ת', 'I': 'י', 'K': 'כ', 'L': 'ל', 'M': 'מ', 'N': 'נ', 'O': '%', 'J': 'ט',
                'S': 'ס', 'E': 'ע', 'P': 'פ', 'C': 'צ', 'Q': 'ק', 'R': 'ר', 'F': 'ש'}

logprob = True

def nullProbability():
    if logprob:
        return float('-inf')
    else:
        return 0
    
def aggregateProbabilities(p1, p2):
    if logprob:
        return p1 + p2
    else:
        return p1 * p2

def transformProbability(p):
    if logprob:
        return math.log(p)
    else:
        return p

def decode(word):
    for sign, letter in signLookup.items():
        word = word.replace(sign, letter)
    for sign, letter in letterLookup.items():
        word = word.replace(sign, letter)
    return word


def analyzeFileQ1(fileName):
    segmentTagPairs = set()
    segmentTagsDict = {}
    segmentCount = 0

    with open(fileName, "r") as f:
        for line in f:
            line = line.strip()
            if line != '':
                segmentCount += 1
                segment, tag = line.split("\t")
                segmentTagPairs.add((segment, tag))
                entryValue = segmentTagsDict.get(segment)
                if entryValue == None:
                    segmentTagsDict[segment] = {tag: 1}
                else:
                    segmentTagsDict[segment][tag] = entryValue.get(tag, 0) + 1
    return segmentTagsDict, segmentTagPairs, segmentCount


def analyzeFileQ2(fileName):
    segmentTagsDict = {}
    unigramDict = {}
    bigramDict = {}
    f = open(fileName, "r")
    unigramCount = 0
    lastTag = '<S>'
    unigramDict[lastTag] = 0
    newLine = True

    num = 5000
    line = f.readline()
    while line:
        line = line.strip()
        if line != '':
            unigramCount += 1
            segment, tag = line.split("\t")
            entryValue = segmentTagsDict.get(segment)
            if entryValue == None:
                segmentTagsDict[segment] = {tag: 1}
            else:
                segmentTagsDict[segment][tag] = entryValue.get(tag, 0) + 1
            unigramDict[tag] = unigramDict.get(tag, 0) + 1
            bigramDict[lastTag + ',' + tag] = bigramDict.get(lastTag + ',' + tag, 0) + 1
            lastTag = tag
            if newLine == True:
                unigramDict['<S>'] = unigramDict.get('<S>', 0) + 1
                newLine = False
            
        else:
            # counting <S> and <E> for current sentence
            unigramCount += 2
            unigramDict['<E>'] = unigramDict.get('<E>', 0) + 1
            bigramDict[lastTag + ',<E>'] = bigramDict.get(lastTag + ',<E>', 0) + 1
            lastTag = '<S>'
            newLine = True
            num -= 1
            if num == 0:
                break
        line = f.readline()
    return segmentTagsDict, unigramDict, bigramDict, unigramCount


def viterbi(sentence, states, emissionProbabilityDict, transitionProbabilityDict):
    v = [{}]
    tags = []
    for state in states:
        transitionProb = transitionProbabilityDict.get('<S>', {}).get(state)
        if transitionProb == None:
            transitionProb = transitionProbabilityDict.get('UNK', {}).get(state, nullProbability())
        emissionProb = emissionProbabilityDict.get(sentence[0])
        if emissionProb != None:
            emissionProb = emissionProb.get(state, nullProbability())
        else:
            emissionProb = emissionProbabilityDict.get('UNK', {}).get(state, nullProbability())
        v[0][state] = aggregateProbabilities(transitionProb, emissionProb), ''
    for i in range(1, len(sentence)):
        v.append({})
        for state1 in states:
            maxProb = nullProbability()
            maxState = ''
            for state2 in states:
                transitionProb = transitionProbabilityDict.get(state2, {}).get(state1)
                if transitionProb == None:
                    transitionProb = transitionProbabilityDict.get('UNK', {}).get(state1, nullProbability())
                if emissionProbabilityDict.get(sentence[i]) != None:
                    emissionProb = emissionProbabilityDict[sentence[i]].get(state1, nullProbability())
                else:
                    emissionProb = emissionProbabilityDict.get('UNK', {}).get(state1, nullProbability())
                currentProb = aggregateProbabilities(aggregateProbabilities(v[i - 1][state2][0], transitionProb), emissionProb)
                if currentProb >= maxProb:
                    maxState = state2
                    maxProb = currentProb
            v[i][state1] = maxProb, maxState
    overallMaxProb = nullProbability()
    overallMaxState = ''
    for i in reversed(range(len(v))):
        for tag, (prob, prevTag) in v[i].items():
            if prob >= overallMaxProb:
                overallMaxProb = prob
                overallMaxState = tag
        if overallMaxProb == nullProbability():
            tags.append('NNP')
        else:
            break
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
    