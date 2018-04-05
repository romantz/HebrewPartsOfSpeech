# -*- coding: utf_8 -*-
import math

signLookup = {'yyCM': ',', 'yyCLN': ':', 'yyLRB': '(', 'yyQUOT': '\"', 'yyDOT': '.', 'yyDASH': '-',
              'yyRRB': ')', 'yyEXCL': '!', 'yyQM': '?', 'yySCLN': ';', 'yyELPS': '...'}

letterLookup = {'A': 'א', 'B': 'ב', 'G': 'ג', 'D': 'ד', 'H': 'ה', 'V': 'ו', 'W': 'ו', 'Z': 'ז', 'U': '\"',
                'X': 'ח', 'T': 'ת', 'I': 'י', 'K': 'כ', 'L': 'ל', 'M': 'מ', 'N': 'נ', 'O': '%', 'J': 'ט',
                'S': 'ס', 'E': 'ע', 'P': 'פ', 'C': 'צ', 'Q': 'ק', 'R': 'ר', 'F': 'ש'}


def decode(word):
    for sign, letter in signLookup.iteritems():
        word = word.replace(sign, letter)
    for sign, letter in letterLookup.iteritems():
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
    count = 0
    lastTag = '<S>'
    unigramDict[lastTag] = 0
    newLine = True

    line = f.readline()
    while line:
        line = line.strip()
        if line != '':
            count += 1
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
    for key, value in bigramDict.iteritems():
        bigramDict[key] = math.log(value / float(unigramDict[key.split(',')[0]]), 10)
    for key, value in unigramDict.iteritems():
        unigramDict[key] = math.log(value / float(count), 10)
    return segmentTagsDict, unigramDict, bigramDict
