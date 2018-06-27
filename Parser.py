import xlrd
import Runner
import logging
import logging.handlers

PARSER_ERROR_LOG_FILENAME = '/mnt/c/Users/Andrew/Desktop/Deloitte/project/Analysis/ParseError.out'

#logger for parsing errors
parseError_Log = logging.getLogger('ErrorLog')
parseError_Log.setLevel(logging.DEBUG)
parseError_Log_handler = logging.handlers.RotatingFileHandler(
              PARSER_ERROR_LOG_FILENAME, maxBytes=2000000, backupCount=5)
parseError_Log.addHandler(parseError_Log_handler)

#ingest the runner data from excel as python objects
#logs parser errors, runners with errors parsing are not returned
#returned runners should be assumed to be valid
def ingestSheet(sheet, enum_gender):
	runners = []
	number_of_rows = sheet.nrows
	number_of_columns = sheet.ncols
	invalidRunnersCount = 0
	for row in range(1, number_of_rows):
		parseError = False
		values = []
		for col in range(number_of_columns):
			value  = (sheet.cell(row,col).value)
			try:
				sanitized_value = Runner.col_sanitizer(col, value)
				values.append(sanitized_value)
			except:
				parseError = True
				values.append(value)
		values.append(enum_gender)
		if parseError: 
			parseError_Log.critical(Runner.Runner(*values))
			invalidRunnersCount+=1
		else: 
			runners.append(Runner.Runner(*values))

	parseError_Log.critical("Invalid %s Runners Count: %d" % (enum_gender, invalidRunnersCount))
	return runners

