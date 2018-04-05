import utils

trainSegmentTagsDict, trainSegmentCount, trainTagSet, trainTagCount = utils.analyzeFile("../data-files/heb-pos.train")
goldSegmentTagsDict, goldSegmentCount, goldTagSet, goldTagCount = utils.analyzeFile("../data-files/heb-pos.gold")

trainAmbiguity = sum(len(x) for x in trainSegmentTagsDict.values()) / float(len(trainSegmentTagsDict))
goldAmbiguity = sum(len(x) for x in goldSegmentTagsDict.values()) / float(len(goldSegmentTagsDict))

print("Train:")
print("Number of segments: {}".format(trainSegmentCount))
print("Number of distinct segments: {}".format(len(trainSegmentTagsDict)))
print("Number of tags: {}".format(trainTagCount))
print("Number of distinct tags: {}".format(len(trainTagSet)))
print("Ambiguity: {}".format(trainAmbiguity))
print("")
print("Gold:")
print("Number of segments: {}".format(goldSegmentCount))
print("Number of distinct segments: {}".format(len(goldSegmentTagsDict)))
print("Number of tags: {}".format(goldTagCount))
print("Number of distinct tags: {}".format(len(goldTagSet)))
print("Ambiguity: {}".format(goldAmbiguity))
