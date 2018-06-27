import xlrd
import glob
import logging
import logging.handlers
import Parser
import Runner
import Analysis
import Plot
import os

#clear contents from last analysis
#if True:
#	files = glob.glob('/mnt/c/Users/Andrew/Desktop/Deloitte/Analysis/*')
#	for f in files:
#	    os.remove(f)

ANALYSIS_LOG_FILENAME = '/mnt/c/Users/Andrew/Desktop/Deloitte/project/Analysis/Analysis.out'

#logger for analysis output
analysis_Log = logging.getLogger('AnalysisLog')
analysis_Log.setLevel(logging.INFO)
analysis_Log_handler = logging.handlers.RotatingFileHandler(
              ANALYSIS_LOG_FILENAME, maxBytes=2000000, backupCount=5)
analysis_Log.addHandler(analysis_Log_handler)

# Open the workbook and define the worksheet
book = xlrd.open_workbook("MA_Exer_PikesPeak.xlsx")

sheet = book.sheet_by_name("MA_Exer_PikesPeak_Males")
maleRunners = Parser.ingestSheet(sheet, "Male")
sheet = book.sheet_by_name("MA_Exer_PikesPeak_Females")
femaleRunners = Parser.ingestSheet(sheet, "Female")

divisions = [[0, 14], [15, 19], [20, 29], [30, 39], [40, 49], [50, 59], [60, 69], [70, 79], [80, 89]]
def getDivision(runner):
	for division in divisions:
		if (division[0] <= runner.int_age <= division[1]):
			return division
	raise Exception("No Division Found")

def doAnalysis(runners, jobName):
	#1. What are the mean, median, mode, and range of the race results for all racers by gender?
	analysis_Log.info(Analysis.AttributeStats(runners, "time_secs_net", jobName))
	analysis_Log.info(Analysis.AttributeStats(runners, "int_age", jobName))
	Plot.plotScatter(jobName, runners, "int_age", "time_secs_net")
	Plot.plotScatter(jobName, runners, "int_age", "time_secs_gun")

	#2. Analyze the difference between gun and net time race results.
	analysis_Log.info("%s time_secs_net difference from time_secs_gun: %f" % (jobName, Analysis.getDifference(runners, Analysis.getMean, "time_secs_net", Analysis.getMean, "time_secs_gun")))

	#4. Compare the race results of each division.
	Plot.plotBinData(jobName, runners, "int_age", "time_secs_net", divisions)


doAnalysis(maleRunners, "Male Runners")
doAnalysis(femaleRunners, "Female Runners")

#do analysis filtering out bad times
maleRunnersAbove500NetSecs = Analysis.findRunnersInRange(maleRunners, "time_secs_net", 500, 10000000)
doAnalysis(maleRunnersAbove500NetSecs, "Male Runners (time_secs_net > 500)")

#do analysis filtering out bad times
femaleRunnersAbove500NetSecs = Analysis.findRunnersInRange(femaleRunners, "time_secs_net", 500, 10000000)
doAnalysis(femaleRunnersAbove500NetSecs, "Female Runners (time_secs_net > 500)")

#3. How much time separates Chris Doe from the top 10 percentile of racers of the same division?
runnersFound = Analysis.findRunners(maleRunners, "string_name", "Chris Doe")
if len(runnersFound) == 1:
	chrisDoeRunner = runnersFound[0]
	chrisDoeDivision = getDivision(chrisDoeRunner)
	chrisDoeDivisionRunners = Analysis.findRunnersInRange(maleRunners, "int_age", chrisDoeDivision[0], chrisDoeDivision[1])
	chrisDoeDivisionRunnersAboveNet500 = Analysis.findRunnersInRange(maleRunners, "time_secs_net", 500, 1000000)
	topTenPercentileRunners = Analysis.getPercentileRunners(chrisDoeDivisionRunnersAboveNet500, "time_secs_net", [0, 10]) #top 10 percent of runners with best time_secs_net
	Plot.plotBinData("Male runners top10% NetSecs>500", topTenPercentileRunners, "int_age", "time_secs_net", divisions)
	topTenPercentileStats = Analysis.AttributeStats(topTenPercentileRunners, "time_secs_net", "%s: Top 10 Percentile Male Runners")
	analysis_Log.info("Net time difference of Chris Doe from top 10%% runners: %f" % (chrisDoeRunner.time_secs_net - topTenPercentileStats.mean))
	Plot.plotScatter("Chris Doe compared to division top10%", topTenPercentileRunners, "int_age", "time_secs_net", markSpecial = [chrisDoeRunner])

#top 10 percentile runners. this will result in a meaningless analysis for #3
#maleRunnersTop10Percentile = Analysis.getPercentileRunners(maleRunners, "time_secs_net", [90, 100])
#doAnalysis(maleRunnersTop10Percentile, "Male Runners (top 10 percentile)")
#femaleRunnersTop10Percentile = Analysis.getPercentileRunners(femaleRunners, "time_secs_net", [90, 100])
#doAnalysis(femaleRunnersTop10Percentile, "Female Runners (top 10 percentile)")

