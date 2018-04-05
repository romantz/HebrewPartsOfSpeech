# -*- coding: utf_8 -*-

signLookup = {'yyCM': ',', 'yyCLN': ':', 'yyLRB': '(', 'yyQUOT': '\"', 'yyDOT': '.', 'yyDASH': '-',
              'yyRRB': ')', 'yyEXCL': '!', 'yyQM': '?', 'yySCLN': ';', 'yyELPS': '...'}

letterLookup = {'A': 'א', 'B': 'ב', 'G': 'ג', 'D': 'ד', 'H': 'ה', 'V': 'ו', 'W': 'ו', 'Z': 'ז', 'U': '\"',
                'X': 'ח', 'T': 'ת', 'I': 'י', 'K': 'כ', 'L': 'ל', 'M': 'מ', 'N': 'נ', 'O': '%', 'J': 'ט',
                'S': 'ס', 'E': 'ע', 'P': 'פ', 'C': 'צ', 'Q': 'ק', 'R': 'ר', 'F': 'ש'}


def decode(word):
    newWord = word
    for sign, letter in signLookup.iteritems():
        newWord = newWord.replace(sign, letter)
    for sign, letter in letterLookup.iteritems():
        newWord = newWord.replace(sign, letter)
    return newWord


def analyzeFile(fileName):
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
