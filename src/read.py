import utils
    
trainSegmentTagsDict, trainSegmentCount, trainTagSet, trainTagCount = utils.analyzeFile("../data-files/heb-pos.train")
goldSegmentTagsDict, goldSegmentCount, goldTagSet, goldTagCount = utils.analyzeFile("../data-files/heb-pos.gold")

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
