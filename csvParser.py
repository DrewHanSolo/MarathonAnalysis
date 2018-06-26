import xlrd
import Runner
import Analysis
import glob
import logging
import logging.handlers
import Plot

LOG_FILENAME = '/mnt/c/Users/Andrew/Desktop/Deloitte/project/logging.out'
# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=5)

my_logger.addHandler(handler)

# Open the workbook and define the worksheet
book = xlrd.open_workbook("MA_Exer_PikesPeak.xlsx")

#ingest the runner data from excel as python objects
def ingestSheet(sheet, enum_gender):
	runners = []
	number_of_rows = sheet.nrows
	number_of_columns = sheet.ncols
	for row in range(1, number_of_rows):
		values = []
		for col in range(number_of_columns):
			value  = (sheet.cell(row,col).value)
			sanitized_value = Runner.col_sanitizer(col, value)
			values.append(sanitized_value)
		values.append(enum_gender)
		runners.append(Runner.Runner(*values))
	return runners


sheet = book.sheet_by_name("MA_Exer_PikesPeak_Males")
maleRunners = ingestSheet(sheet, "Male")
sheet = book.sheet_by_name("MA_Exer_PikesPeak_Females")
femaleRunners = ingestSheet(sheet, "Female")

[validRunners, invalidRunners] = Analysis.splitValidInvalidRunners(maleRunners)
#log the invalid runners and their attributes
for invalidRunner in invalidRunners:
	my_logger.debug(invalidRunner)

Analysis.sortRunnersByNetTime(validRunners)
#for runner in validRunners:
#	print(runner)
#print(Analysis.getMean(validRunners, ))


#print(Analysis.getMean(validRunners, 'int_place'))
#print(Analysis.getMean(validRunners, 'string_div_total'))
#print(Analysis.getMean(validRunners, 'int_num'))
#print(Analysis.getMean(validRunners, 'string_name'))
#print(Analysis.getMean(validRunners, 'int_age'))
#print(Analysis.getMean(validRunners, 'string_hometown'))
print(Analysis.getMean(validRunners, 'time_secs_gun'))
print(Analysis.getMean(validRunners, 'time_secs_net'))
print(Analysis.getMean(validRunners, 'time_secs_pace'))
print(Analysis.getMode(validRunners, 'time_secs_gun'))
print(Analysis.getMode(validRunners, 'time_secs_net'))
print(Analysis.getMode(validRunners, 'time_secs_pace'))
print(Analysis.getMedian(validRunners, 'time_secs_gun'))
print(Analysis.getMedian(validRunners, 'time_secs_net'))
print(Analysis.getMedian(validRunners, 'time_secs_pace'))

Plot.plotScatter("Male Runners", validRunners, "int_age", "time_secs_net")
