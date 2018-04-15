import utils

trainSegmentTagsDict, trainSegmentTagPairs, trainSegmentCount = utils.analyzeFileQ1("../data-files/heb-pos.train")
goldSegmentTagsDict, goldSegmentTagPairs, goldSegmentCount = utils.analyzeFileQ1("../data-files/heb-pos.gold")

trainAmbiguity = sum(len(x) for x in trainSegmentTagsDict.values()) / float(len(trainSegmentTagsDict))
goldAmbiguity = sum(len(x) for x in goldSegmentTagsDict.values()) / float(len(goldSegmentTagsDict))

print('Train:')
print('Number of segments: {}'.format(trainSegmentCount))
print('Number of distinct segments: {}'.format(len(trainSegmentTagsDict)))
print('Number of segment tag pairs: {}'.format(trainSegmentCount))
print('Number of distinct segment tag pairs: {}'.format(len(trainSegmentTagPairs)))
print('Ambiguity: {}'.format(trainAmbiguity))
print('')
print('Gold:')
print('Number of segments: {}'.format(goldSegmentCount))
print('Number of distinct segments: {}'.format(len(goldSegmentTagsDict)))
print('Number of segment tag pairs: {}'.format(goldSegmentCount))
print('Number of distinct segment tag pairs: {}'.format(len(goldSegmentTagPairs)))
print('Ambiguity: {}'.format(goldAmbiguity))
