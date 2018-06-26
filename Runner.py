class Runner(object):
	def __init__(self, int_place, string_div_total, string_name, int_num, int_age, string_hometown, time_secs_gun, time_secs_net, time_secs_pace, enum_sex):
		self.int_place = int_place
		self.string_div_total = string_div_total
		self.int_num = int_num
		self.string_name = string_name
		self.int_age = int_age
		self.string_hometown = string_hometown
		self.time_secs_gun = time_secs_gun
		self.time_secs_net = time_secs_net
		self.time_secs_pace = time_secs_pace
		self.enum_sex = enum_sex

	def __str__(self):
		return("Runner object:\n"
			"  Place = {0}\n"
			"  Div/Total = {1}\n"
			"  Num = {2}\n"
			"  Name = {3}\n"
			"  Age = {4}\n"
			"  Hometown = {5} \n"
			"  Gun = {6} \n"
			"  Net = {7} \n"
			"  Pace = {8} \n"
			"  Sex = {9} \n"
			.format(self.int_place, self.string_div_total, self.string_name, self.int_num,
				self.int_age, self.string_hometown, self.time_secs_gun, self.time_secs_net, self.time_secs_pace, self.enum_sex))

def stringLiteralTimeToSecs(argument):
	ftr = [3600,60,1]
	return int(sum([int(a)*int(b) for a,b in zip(ftr, map(int,str(argument).split(':')))]))

def col_sanitizer(columnIndex, argument):
	try:
		if columnIndex == 0:
			return int(argument)	# int_place
		if columnIndex == 1:
			return str(argument)	# string_div_total
		if columnIndex == 2:
			return int(argument)	# int_num
		if columnIndex == 3:
			return str(argument)	# string_name
		if columnIndex == 4:
			return int(argument)	# int_age
		if columnIndex == 5:
			return str(argument)	# string_hometown
		if columnIndex == 6:
			return stringLiteralTimeToSecs(argument)	# time_secs_gun
		if columnIndex == 7:
			return stringLiteralTimeToSecs(argument)	# time_secs_net
		if columnIndex == 8:
			return stringLiteralTimeToSecs(argument)	# time_secs_pace
	except:
		return "N/A"