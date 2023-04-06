from datetime import datetime
import mysql.connector
from ftplib import FTP
import traceback
from func_timeout import func_timeout, FunctionTimedOut

def sql_initialize(verbose=False, t_out=5):
	'''
	Connect to the sql server and return a cursor
	
	Parameters:
	-----------
	verbose: bool
		Set true for more detail error message
		
	Returns:
	-----------
	sql_inited: bool
		A flag on whether the initialization is successful
	mydb: mysql.connector
		The connection to the mysql

	'''
	
	t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
	
	try:
		
		mydb = mysql.connector.connect(
		host="192.168.100.1",
		user="ailand",
		password="etarob",
		database="handwagen",
		connection_timeout = t_out,
		)
		print(t, ": successfully connected to mysql")
		sql_inited = True
		
	except:

		if verbose:
			print(traceback.format_exc())
		
		else:
			print(t, ": unable to connect to mysql")
		
		sql_inited = False
		mydb = None
		
	return sql_inited, mydb

def get_all_value(mydb, sql_inited, verbose=True, t_out=5):
	'''
	Read the values from the sql server
	
	Parameters:
	-----------
	mydb: mysql.connector
		The connection to the mysql
	sql_inited: bool
		Flag to set to false if the function fails
	verbose: bool
		Enable this for more detail error message
		
	Returns:
	--------
	control_result: array
		The table of control
	arducam_result: array
		The table of arducam_camera
	daheng_result: array
		The table of daheng_camera
	sql_inited: bool
		Return false if fail to get value in sql
	
	'''
	
	def _get_all_value(mydb):
		mycursor = mydb.cursor()
		mycursor.execute("SELECT * FROM control")
		control_result = mycursor.fetchall()[0]
		mycursor.execute("SELECT * FROM arducam_camera")
		arducam_result = mycursor.fetchall()[0]
		mycursor.execute("SELECT * FROM daheng_camera")
		daheng_result = mycursor.fetchall()[0]
		mydb.commit()
		
		return control_result, arducam_result, daheng_result
	
	t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
		
	try:
		
		control_result, arducam_result, daheng_result = func_timeout(t_out, _get_all_value, args=[mydb])
	
	except:
		
		if verbose:
			print(traceback.format_exc())
		else:
			print(t, ": unable to get all value from mysql")

		sql_inited = False
		control_result = None
		arducam_result = None
		daheng_result = None
			
	return sql_inited, control_result, arducam_result, daheng_result

def set_value(mydb, sql_inited, table, var_name, value, verbose=True, t_out=5):
	'''
	Read the values from the sql server
	
	Parameters:
	-----------
	mydb: mysql.connector
		The connection to the mysql
	sql_inited: bool
		Flag to set to false if the function fails
	table: str
		Table name in the sql databank
	var_name: str
		The column in the sql databank
	value: str
		The value in the sql databank
	verbose: bool
		Enable this for more detail error message
		
	Returns:
	--------
	sql_inited: bool
		Return false if fail to write value in sql
	
	'''
	def _set_value(mydb, table, var_name, value):
		mycursor = mydb.cursor()
		sql_cmd = "UPDATE " + table + " SET " + var_name + " = " + value + " WHERE 1"
		mycursor.execute(sql_cmd)
		mydb.commit()
	
	t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
		
	try:
		
		func_timeout(5, _set_value, args=[mydb, table, var_name, value])
	
	except:
		
		if verbose:
			print(traceback.format_exc())
		else:
			print(t, ": unable to set value in mysql")

		sql_inited = False
	
	return sql_inited
	
def get_value(mydb, sql_inited, table, var_name, verbose=True, t_out=5):
	'''
	Read the values from the sql server
	
	Parameters:
	-----------
	mydb: mysql.connector
		The connection to the mysql
	sql_inited: bool
		Flag to set to false if the function fails
	table: str
		Table name in the sql databank
	var_name: str
		The column in the sql databank
	verbose: bool
		Enable this for more detail error message
		
	Returns:
	--------
	sql_inited: bool
		Return false if fail to write value in sql
	sql_var: str
		The value in the sql databank
	
	'''
	def _get_value(mydb, table, var_name):
		mycursor = mydb.cursor()
		sql_cmd = "SELECT " + var_name + " FROM " + table + " WHERE 1"
		mycursor.execute(sql_cmd)
		sql_var = mycursor.fetchall()[0][0]
		mydb.commit()
		
		return sql_var
	
	t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
		
	try:
		
		sql_var = func_timeout(t_out, _get_value, args=[mydb, table, var_name])
	
	except:
		
		if verbose:
			print(traceback.format_exc())
		else:
			print(t, ": unable to get value", var_name, " in mysql")

		sql_var = None
		sql_inited = False
	
	return sql_inited, sql_var
	
def ftp_initialize(verbose=False, t_out=5):
	'''
	Initialize the sql server
	
	Parameters:
	-----------
	verbose: bool
		Enable this for more detail error message
		
	Returns:
	--------
	ftp_inited: bool
		A flag on whether the initialization is successful
	
	'''
	
	t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
	
	try:
		
	  ftp = FTP('192.168.100.1', timeout=t_out)
	  ftp.login('ailand', 'etarob')
	  print(t, ": successfully connected to ftp server")
	  ftp_inited = True
	  
	except:
		
	  ftp = None
	  print(t, ": unable to connect to ftp")
	  ftp_inited = False
	  
	  if verbose:
		  print(traceback.format_exc())
	
	return ftp_inited, ftp
