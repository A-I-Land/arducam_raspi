from picamera2 import Picamera2, Preview
from cameraSetup import *
import cv2
from libcamera import controls
from ftplib import FTP
from io import BytesIO
import RPi.GPIO as gpio
import mysql.connector
import time
import traceback

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
  print("arducam calibration successful")

def get_sql():
  '''
  Read the values from the sql server
  '''
  mycursor.execute("SELECT * FROM control")
  control_result = mycursor.fetchall()[0]
  mycursor.execute("SELECT * FROM arducam_camera")
  arducam_result = mycursor.fetchall()[0]
  
  return control_result[0], control_result[1], control_result[2], control_result[3], arducam_result[0]
    
def set_hard(flag):
  '''
  Set the values for the hard trigger
  '''
  sql_cmd = "UPDATE control SET hard_capture = " + str(flag) + " WHERE 1"
  mycursor.execute(sql_cmd)
  mydb.commit()

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
  
def set_image(flag):
  '''
  Set the value for whether the arducam is on
  '''
  sql_cmd = "UPDATE control SET get_image = " + str(flag) + " WHERE 1"
  mycursor.execute(sql_cmd)
  mydb.commit()
  
# Flags
initialized = False
init_arducam = False
init_sql = False
init_ftp = False

## Setting up the GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT) #trigger for gate driver
gpio.setup(27, gpio.OUT) #enable gate driver
gpio.setup(4, gpio.IN, pull_up_down=gpio.PUD_DOWN)

gpio.output(17, True)
gpio.output(27, False)

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
  
  ## Arducam ------------------------------------------------
  if not init_arducam:
    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration(main={"size": (4656, 3496)}, lores={"size": (640, 480)}, display="lores", queue=False)
    picam2.configure(capture_config)
    picam2.set_controls({"ExposureTime": ardu_expo, "AfMode": controls.AfModeEnum.Auto, "AwbEnable": True})
    picam2.start()
    calibration()
    init_arducam = True
    print(loop_t, ": successfully initialized camera")
      
  ## MySQL ---------------------------------------------------
  if sql and not init_sql:
    try:
      mydb = mysql.connector.connect(
        host="192.168.100.1",
        user="ailand",
        password="etarob",
        database="handwagen"
      )
      print(loop_t, ": successfully connected to mysql")
      init_sql = True
      mycursor = mydb.cursor()
    except:
      print(traceback.format_exc())
      print(loop_t, ": unable to connect to sql")

  ## Connect to FTP ------------------------------------------
  if ftp_enable and not init_ftp:
    try:
      ftp = FTP('192.168.100.1')
      ftp.login('ailand', 'etarob')
      print(loop_t, ": successfully connected to ftp server")
      init_ftp = True
    except:
      print(traceback.format_exc())
      print(loop_t, ": unable to connect to ftp")
      
  if sql and init_sql:
    soft_capture, hard_capture, image_name, do_calibration, ardu_expo = get_sql()
    
  # calibration with sql
  if do_calibration:
    print(loop_t, ": calibrate through mysql")
    calibration()
    set_calibrate(0)
  
  # detect hardware trigger
  if gpio.input(4) == gpio.HIGH:
    print(loop_t, ": button pressed")
    if sql and init_sql: set_hard(1)
  else:
    if sql and init_sql: set_hard(0)
    
  # capturing
  if soft_capture:
          
    ardu_img = picam2.capture_array("main")
    ardu_img = cv2.cvtColor(ardu_img, cv2.COLOR_RGB2BGR)
    
    t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
    
    if init_ftp:
      retval_1, buffer_1 = cv2.imencode(".jpg", ardu_img)
      flo1 = BytesIO(buffer_1)
      try:
        ftp.storbinary('STOR arducam/' + image_name, flo1)
        print(loop_t, ": Done saving 16mp picture via ftp")
      except:
        print(traceback.format_exc())
        print(loop_t, ": Unable to save via ftp, resort to local save")
        init_ftp = False
        cv2.imwrite("/home/ailand/Pictures/arducam/" + t + ".jpg", ardu_img)
    
    else:
      print(loop_t, ": Done saving 16mp picture locally")
      cv2.imwrite("/home/ailand/Pictures/arducam/" + t + ".jpg", ardu_img)
      
      
    if sql and init_sql: set_soft(0)
    
  else:
    
    ardu_img = picam2.capture_array("lores")
    ardu_img = ardu_img[0:480, :] # image has to be cropped because some problem with capture array
    
    if init_ftp:
      retval2, buffer2 = cv2.imencode(".jpg", ardu_img)
      flo2 = BytesIO(buffer2)
      try:
        ftp.storbinary('STOR preview/preview.jpg', flo2)
        print(loop_t, ": Done sending preview picture via ftp")
      except:
        print(traceback.format_exc())
        print(loop_t, ": Unable to save via ftp, resort to local save")
        cv2.imwrite("/home/ailand/Pictures/preview/preview.jpg", ardu_img)
        init_ftp = False

    else:
      print(loop_t, ": Done saving preview picture locally")
      cv2.imwrite("/home/ailand/Pictures/preview/preview.jpg", ardu_img)
