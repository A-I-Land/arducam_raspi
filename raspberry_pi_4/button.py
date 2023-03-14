import RPi.GPIO as gpio
from datetime import datetime
import traceback
from func_timeout import func_timeout, FunctionTimedOut
import mysql.connector
import time
from commonFunctions import sql_initialize, ftp_initialize, get_all_value, set_value, get_value

## Setting up the GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_UP)

# User inputs
debug = False

# Variables
sql_inited = False
control = [0, 0, 0, 0]
daheng = [0, 0, 0, 0]
arducam = [0, 0, 0, 0]
	
while True:
	
	loop_t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
	
	# Initialize the sql
	if not sql_inited:
		sql_inited, mydb = sql_initialize()
	
	# Get value from sql
	if sql_inited:	
		sql_inited, control, arducam, daheng = get_all_value(mydb, sql_inited)
		
	# Set soft_capture to 0 if both camera had captured
	if daheng[3]:
		sql_inited = set_value(mydb, sql_inited, 'control', 'soft_capture', '0')
		sql_inited = set_value(mydb, sql_inited, 'arducam_camera', 'capture', '0')
		sql_inited = set_value(mydb, sql_inited, 'daheng_camera', 'capture', '0')
		
	# Detect button press		
	if gpio.input(17) == gpio.LOW:
		print(loop_t, ": button pressed")
		if sql_inited:
			sql_inited = set_value(mydb, sql_inited, 'control', 'hard_capture', '1')
	else:
		if sql_inited: 
		  sql_inited = set_value(mydb, sql_inited, 'control', 'hard_capture', '0')
			  
