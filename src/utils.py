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
    segmentTagsDict = {}
    tagSet = set()
    segmentCount = 0
    tagCount = 0

    with open(fileName, "r") as f:
        for line in f:
            line = line.strip()
            if line != '':
                segmentCount += 1
                segment, tag = line.split("\t")
                tagSet.add(tag)
                tagCount += 1

                entryValue = segmentTagsDict.get(segment)
                if entryValue == None:
                    segmentTagsDict[segment] = {tag: 1}
                else:
                    segmentTagsDict[segment][tag] = entryValue.get(tag, 0) + 1
    return segmentTagsDict, segmentCount, tagSet, tagCount


def analyzeFileQ2(fileName):
    segmentTagsDict = {}
    unigramDict = {}
    bigramDict = {}
    f = open(fileName, "r")
    unigramCount = 0
    lastTag = '<S>'
    unigramDict[lastTag] = 0
    newLine = True

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
            unigramDict['<E>'] = unigramDict.get('<E>', 0) + 1
            bigramDict[lastTag + ',<E>'] = bigramDict.get(lastTag + ',<E>', 0) + 1
            lastTag = '<S>'
            newLine = True
        line = f.readline()
#    for key, value in bigramDict.items():
#        bigramDict[key] = math.log(value / float(unigramDict[key.split(',')[0]]))
#    for key, value in unigramDict.items():
#        unigramDict[key] = math.log(value / float(count))
    return segmentTagsDict, unigramDict, bigramDict, unigramCount


def viterbi(sentence, states, emissionProbabilityDict, transitionProbabilityDict):
    v = [{}]
    b = []
    tags = []
    for state in states:
        v[0][state] = aggregateProbabilities(transitionProbabilityDict['<S>'].get(state, nullProbability()), emissionProbabilityDict.get(sentence[0], {}).get(state, nullProbability()))
    for i in range(1, len(sentence)):
        v.append({})
        b.append({})
        for state1 in states:
            maxProb = nullProbability()
            maxState = ''
            for state2 in states:
                currentProb = aggregateProbabilities(aggregateProbabilities(v[i - 1][state2], transitionProbabilityDict.get(state2, {}).get(state1, nullProbability())), emissionProbabilityDict.get(sentence[i], {}).get(state1, nullProbability()))
                if currentProb >= maxProb:
                    maxState = state2
                    maxProb = currentProb
            v[i][state1] = maxProb
            b[i-1][state1] = maxState
    overallMaxProb = nullProbability()
    overallMaxState = ''
    for key, value in v[len(v) - 1].items():
        if value >= overallMaxProb:
            overallMaxProb = value
            overallMaxState = key
    tags.append(overallMaxState)
    lastTag = overallMaxState
    for i in reversed(range(len(b))):
        newTag = b[i][lastTag]
        tags.append(newTag)
        lastTag = newTag
    return list(reversed(tags))
    