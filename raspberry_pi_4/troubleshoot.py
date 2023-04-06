from commonFunctions import sql_initialize, ftp_initialize, get_all_value, set_value, get_value
import traceback

sql_inited = False

while True:
	try:
		if not sql_inited:
			print("initializing")
			sql_inited, mydb = sql_initialize(verbose=True, t_out=0.1)
		else:
			print("setting")
			sql_inited = set_value(mydb, sql_inited, 'control', 'hard_capture', '0', verbose=True, t_out=0.1)

	except:
		print(traceback.format_exc())
		sql_inited = False
