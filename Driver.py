import xlrd
import glob
import logging
import logging.handlers
import Parser
import Runner
import Analysis
import Plot

LOG_FILENAME = '/mnt/c/Users/Andrew/Desktop/Deloitte/Analysis/logging.out'
# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=2000000, backupCount=5)

my_logger.addHandler(handler)

# Open the workbook and define the worksheet
book = xlrd.open_workbook("MA_Exer_PikesPeak.xlsx")

sheet = book.sheet_by_name("MA_Exer_PikesPeak_Males")
maleRunners = Parser.ingestSheet(sheet, "Male")
sheet = book.sheet_by_name("MA_Exer_PikesPeak_Females")
femaleRunners = Parser.ingestSheet(sheet, "Female")

divisions = [[0, 14], [15, 19], [20, 29], [30, 39], [40, 49], [50, 59], [60, 69], [70, 79], [80, 89], [90, 99], [100, 110]]

def doAnalysis(runners, jobName):
	[validRunners, invalidRunners] = Analysis.splitValidInvalidRunners(runners)

	#log the invalid runners and their attributes
	#for invalidRunner in invalidRunners:
	#	my_logger.debug(invalidRunner)

	#1. What are the mean, median, mode, and range of the race results for all racers by gender?
	my_logger.info(Analysis.AttributeStats(validRunners, "time_secs_net", jobName))
	my_logger.info(Analysis.AttributeStats(validRunners, "int_age", jobName))
	Plot.plotScatter(jobName, validRunners, "int_age", "time_secs_net")
	Plot.plotScatter(jobName, validRunners, "int_age", "time_secs_gun")

	#2. Analyze the difference between gun and net time race results.
	my_logger.info("%s time_secs_net difference from time_secs_gun: %f" % (jobName, Analysis.getDifference(validRunners, Analysis.getMean, "time_secs_net", Analysis.getMean, "time_secs_gun")))

	#3. How much time separates Chris Doe from the top 10 percentile of racers of the same division?
	runnersFound = Analysis.findRunners(validRunners, "string_name", "Chris Doe")
	if len(runnersFound) == 1:
		chrisDoeRunner = runnersFound[0]
		topTenPercentileRunners = Analysis.getPercentileRunners(validRunners, "time_secs_net", [90, 100])
		topTenPercentileStats = Analysis.AttributeStats(topTenPercentileRunners, "time_secs_net", "Top 10 Percentile Male Runners")
		my_logger.info("Net time difference of Chris Doe from top 10%% runners: %f" % (chrisDoeRunner.time_secs_net - topTenPercentileStats.mean))

	#4. Compare the race results of each division.
	Plot.plotBinData(jobName, validRunners, "int_age", "time_secs_net", divisions)


doAnalysis(maleRunners, "Male Runners")
doAnalysis(femaleRunners, "Female Runners")

#do analysis filtering out bad times
[validMaleRunners, invalidRunners] = Analysis.splitValidInvalidRunners(maleRunners)
maleRunnersAbove500NetSecs = Analysis.findRunnersInRange(validMaleRunners, "time_secs_net", 500, 10000000)
doAnalysis(maleRunnersAbove500NetSecs, "Male Runners (time_secs_net > 500)")

#do analysis filtering out bad times
[validFemaleRunners, invalidRunners] = Analysis.splitValidInvalidRunners(femaleRunners)
femaleRunnersAbove500NetSecs = Analysis.findRunnersInRange(validFemaleRunners, "time_secs_net", 500, 10000000)
doAnalysis(femaleRunnersAbove500NetSecs, "Female Runners (time_secs_net > 500)")


