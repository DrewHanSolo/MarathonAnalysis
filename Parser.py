import xlrd
import Runner

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

