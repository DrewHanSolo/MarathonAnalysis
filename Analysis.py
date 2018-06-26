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


def sortRunnersByNetTime(runners):
	runners.sort(key=lambda x: int(x.time_secs_net), reverse=True)



#returns a list of a particular attribute for all runners
def getAttributes(runners, attribute):
	vals = []
	for runner in runners:
		vals.append(getattr(runner, attribute))
	return vals

def getMean(runners, attribute):
	return sum(getAttributes(runners, attribute)) / len(runners)

def getMedian(runners, attribute):
	return numpy.median(getAttributes(runners, attribute))

def getMode(runners, attribute):
	vals = getAttributes(runners, attribute)
	return max(set(vals), key=vals.count)