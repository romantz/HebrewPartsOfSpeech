import utils

def analyzeFile(fileName):    
    segmentTagsDict = {}
    tagSet = set()
    segmentCount = 0
    tagCount = 0
    f = open(fileName, "r")
    
    for line in f:
        line = line.strip()
        if line != '':
            segmentCount += 1
            segment, tag = line.split("\t")
            if utils.signLookup.get(tag) == None:
                tagSet.add(tag)
                tagCount += 1
            
            entryValue = segmentTagsDict.get(segment)
            if entryValue == None:
                segmentTagsDict[segment] = {tag: 1}
            else:
                segmentTagsDict[segment][tag] = entryValue.get(tag, 0) + 1
    f.close()
    return segmentTagsDict, segmentCount, tagSet, tagCount
    
trainSegmentTagsDict, trainSegmentCount, trainTagSet, trainTagCount = analyzeFile("../data-files/heb-pos.train")
goldSegmentTagsDict, goldSegmentCount, goldTagSet, goldTagCount = analyzeFile("../data-files/heb-pos.gold")

trainAmbiguity = sum(map(lambda x: len(x), trainSegmentTagsDict.values())) / float(len(trainSegmentTagsDict))
goldAmbiguity = sum(map(lambda x: len(x), goldSegmentTagsDict.values())) / float(len(goldSegmentTagsDict))

print "Train:"
print "Number of segments: " + str(trainSegmentCount)
print "Number of distinct segments: " + str(len(trainSegmentTagsDict))
print "Number of tags: " + str(trainTagCount)
print "Number of distinct tags: " + str(len(trainTagSet))
print "Ambiguity: " + str(trainAmbiguity)
print ""
print "Gold:"
print "Number of segments: " + str(goldSegmentCount)
print "Number of distinct segments: " + str(len(goldSegmentTagsDict))
print "Number of tags: " + str(goldTagCount)
print "Number of distinct tags: " + str(len(goldTagSet))
print "Ambiguity: " + str(goldAmbiguity)
