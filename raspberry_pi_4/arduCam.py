from picamera2 import Picamera2, Preview
from cameraSetup import *
import cv2
from libcamera import controls
from ftplib import FTP
from io import BytesIO
import mysql.connector
import time
import traceback
from func_timeout import func_timeout, FunctionTimedOut

# User variables  
ftp_enable = True # Enable this to save to ftp, else save locally
sql = True # Enable this to connect to sql

def calibration():
  '''
  Calibrate all the cameras
  '''
  print("start arducam calibration")
  picam2.stop()
  picam2.set_controls({"ExposureTime": ardu_expo, "AfMode": controls.AfModeEnum.Auto, "AwbEnable": True})
  picam2.start()
  success = picam2.autofocus_cycle()
  func_timeout(1, set_calibrate, args=('0'))
  print("arducam calibration successful")

def get_sql():
  '''
  Read the values from the sql server
  '''
  mycursor.execute("SELECT * FROM control")
  control_result = mycursor.fetchall()[0]
  mycursor.execute("SELECT * FROM arducam_camera")
  arducam_result = mycursor.fetchall()[0]
  mycursor.execute("SELECT * FROM daheng_camera")
  daheng_result = mycursor.fetchall()[0]
  mydb.commit()
  
  return control_result, arducam_result, daheng_result
    
def set_soft(flag):
  '''
  Set the values for the soft trigger
  '''
  sql_cmd = "UPDATE control SET soft_capture = " + str(flag) + " WHERE 1"
  mycursor.execute(sql_cmd)
  mydb.commit()

def set_calibrate(flag):
  '''
  Set the values for the soft trigger
  '''
  sql_cmd = "UPDATE control SET do_calibration = " + str(flag) + " WHERE 1"
  mycursor.execute(sql_cmd)
  mydb.commit()

def set_value(table, var_name, value):
	'''
	Set the values for the soft trigger
	'''
	sql_cmd = "UPDATE " + table + " SET " + var_name + " = " + value + " WHERE 1"
	mycursor.execute(sql_cmd)
	mydb.commit()
  
# Flags
initialized = False
init_arducam = False
init_sql = False
init_ftp = False

# variable in sql
do_capture = 0
do_calibration = 0
ardu_expo = 10000
soft_capture = False
daheng_capture = False
ardu_capture = False
get_image_sql = 0
            
while True:
  
  loop_t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
  
  ## MySQL ---------------------------------------------------
  if sql and not init_sql:
    try:
      mydb = mysql.connector.connect(
        host="192.168.100.1",
        user="ailand",
        password="etarob",
        database="handwagen",
        connection_timeout = 20,
      )
      print(loop_t, ": successfully connected to mysql")
      init_sql = True
      mycursor = mydb.cursor()
    except:
      print(traceback.format_exc())
      print(loop_t, ": unable to connect to sql")
      init_sql = False
  
  ## Connect to FTP ------------------------------------------
  if ftp_enable and not init_ftp:
    try:
      ftp = FTP('192.168.100.1', timeout=5)
      ftp.login('ailand', 'etarob')
      print(loop_t, ": successfully connected to ftp server")
      init_ftp = True
    except:
      print(traceback.format_exc())
      print(loop_t, ": unable to connect to ftp")
  
  ## Get values from sql    
  if sql and init_sql:
    try:
      control, arducam, daheng = func_timeout(1, get_sql)
    except:
      print(traceback.format_exc())
      print(loop_t, ": connection to sql broken")
      init_sql = False
  
  ## Arducam ------------------------------------------------
  if not init_arducam:
    
    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration(main={"size": (4656, 3496)}, lores={"size": (640, 480)}, display="lores", queue=False)
    picam2.configure(capture_config)
    picam2.set_controls({"ExposureTime": ardu_expo, "AfMode": controls.AfModeEnum.Auto, "AwbEnable": True})
    picam2.start()
    calibration()
    
    init_arducam = True
    print(loop_t, ": succesfully initialized arducam")
    
  # calibration with sql
  if control[3]:
    print(loop_t, ": calibrate through mysql")
    calibration()
      
  # capturing
  if control[0] and not arducam[4]:
          
    ardu_img = picam2.capture_array("main")
    ardu_img = cv2.cvtColor(ardu_img, cv2.COLOR_RGB2BGR)
    
    t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
    
    # save picture
    if init_ftp:
      retval_1, buffer_1 = cv2.imencode(".jpg", ardu_img)
      flo1 = BytesIO(buffer_1)
      try:
        ftp.storbinary('STOR arducam/' + control[2], flo1)
        print(loop_t, ": Done saving 16mp picture via ftp")
      except:
        print(traceback.format_exc())
        print(loop_t, ": Unable to save via ftp, resort to local save")
        init_ftp = False
        cv2.imwrite("/home/ailand/Pictures/arducam/" + image_name + ".jpg", ardu_img)
    
    else:
      print(loop_t, ": Done saving 16mp picture locally")
      cv2.imwrite("/home/ailand/Pictures/arducam/" + t + ".jpg", ardu_img)
      
    # set the capture back to 0
    if sql and init_sql: 
      try:
        func_timeout(1, set_value, args=('arducam_camera', 'capture', '1'))
      except:
        print(traceback.format_exc())
        print(loop_t, ": connection to sql broken")
        init_sql = False
