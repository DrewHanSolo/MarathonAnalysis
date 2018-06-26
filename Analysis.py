import Runner
import numpy

def splitValidInvalidRunners(runners):
	validRunners = []
	invalidRunners = []
	for runner in runners:
		if ((runner.time_secs_gun == "N/A") or (runner.time_secs_net == "N/A") or (runner.time_secs_pace == "N/A") or (runner.int_age == "N/A")):
			invalidRunners.append(runner)
			continue
		validRunners.append(runner)
	return [validRunners, invalidRunners]

def findRunners(runners, attribute, attribute_val):
	returnRunners = []
	for runner in runners:
		if (getattr(runner, attribute) == attribute_val):
			returnRunners.append(runner)
	return returnRunners

def findRunnersInRange(runners, attribute, attribute_val_min, attribute_val_max):
	returnRunners = []
	for runner in runners:
		val = getattr(runner, attribute);
		if (attribute_val_min <= val <= attribute_val_max):
			returnRunners.append(runner)
	return returnRunners

def sortRunnersByNetTime(runners):
	runners.sort(key=lambda x: int(x.time_secs_net), reverse=True)

def getRange(runners, attribute):
	if (len(runners) == 0):
		return [0, 0]
	vals = getAttributes(runners, attribute)
	return [min(vals), max(vals)]

#returns a list of a particular attribute for all runners
def getAttributes(runners, attribute):
	vals = []
	for runner in runners:
		vals.append(getattr(runner, attribute))
	return vals

def getMean(runners, attribute):
	if (len(runners) == 0):
		return 0
	return sum(getAttributes(runners, attribute)) / len(runners)

def getMedian(runners, attribute):
	return numpy.median(getAttributes(runners, attribute))

def getMode(runners, attribute):
	if (len(runners) == 0):
		return 0
	vals = getAttributes(runners, attribute)
	return max(set(vals), key=vals.count)

def getDifference(runners, func1, attribute1, func2, attribute2):
	val1 = func1(runners, attribute1);
	val2 = func2(runners, attribute2);
	return (val1 - val2)

def getMeanMedianModeRange(runners, attribute):
	mean = getMean(runners, attribute)
	median = getMedian(runners, attribute)
	mode = getMode(runners, attribute)
	rangeVal = getRange(runners, attribute)
	return [mean, median, mode, rangeVal]

class AttributeStats(object):
	def __init__(self, runners, attribute, name = ""):
		[mean, median, mode, rangeVal] = getMeanMedianModeRange(runners, attribute)
		self.name = name #id of this stat
		self.attribute = attribute #attribute of this stat
		self.mean = mean
		self.median = median
		self.mode = mode
		self.stdDev = numpy.std(getAttributes(runners, attribute))
		self.rangeVal = rangeVal
		self.count = len(runners)

	def __str__(self):
		return("{0}:\n"
			"  Attribute = {1}\n"
			"  Mean = {2}\n"
			"  Standard Dev = {3}\n"
			"  Median = {4}\n"
			"  Mode = {5}\n"
			"  Range = {6}\n"
			"  Count = {7} \n"
			.format(self.name, self.attribute, self.mean, self.stdDev, self.median,
				self.mode, self.rangeVal, self.count))


def getBinData(runners, binProperty, dataProperty, bins):
	if len(runners) == 0:
		return 0, 0, 0, 0, 0, 0

	avgs = []
	stdDevs = []
	stdErrs = []
	trackCounts = []
	countPercents = []
	binCenters = []

	attributeStats = []
	for binRange in bins:
		binnedRunners = findRunnersInRange(runners, binProperty, binRange[0], binRange[1])
		attributeStats.append(AttributeStats(binnedRunners, dataProperty, "%s binned by %s" % (dataProperty, binProperty)))

	for attributeStat in attributeStats:
		avgs.append(attributeStat.mean)
		stdDevs.append(attributeStat.stdDev)

	for binRange in bins:
		binCenters.append((binRange[0] + binRange[1]) / 2)

	return avgs, stdDevs, binCenters

#returns runners whose data of property falls within the percentileRange
def getPercentileRunners(runners, propertyName, percentileRange):
	percentileVals = numpy.percentile(getAttributes(runners, propertyName), percentileRange)
	returnRunners = []
	for runner in runners:
		val = getattr(runner, propertyName)
		if (percentileVals[0] <= val <= percentileVals[1]):
			returnRunners.append(runner)
	return returnRunners
