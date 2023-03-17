from cameraSetup import *
import traceback
import cv2
from io import BytesIO
from func_timeout import func_timeout, FunctionTimedOut
from commonFunctions import sql_initialize, ftp_initialize, get_all_value, set_value, get_value

# User inputs
debug = False
sql_enable = True
ftp_enable = True

# Variables

# Module variables
cam_inited = False
sql_inited = False
ftp_inited = False
control = [0, 0, 0, 0]
daheng = [0, 0, 0, 0, 0]
arducam = [0, 0, 0, 0]

while True:
	
	loop_t = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
	
	# Initialize the sql
	if sql_enable and not sql_inited:
		
		sql_inited, mydb = sql_initialize()
		
	# Initialize the ftp
	if ftp_enable and not ftp_inited:
		
		ftp_inited, ftp = ftp_initialize()
	
	# Get variable value from sql
	if sql_enable and sql_inited:
		
		sql_inited, control, arducam, daheng = get_all_value(mydb, sql_inited)
				
	# Initialize the daheng camera
	if not cam_inited and sql_inited:
		
		try:
			
			device_manager = get_deviceManagerGX()
			cams = []
			cams = get_cams_byIndex(device_manager, cams)
			init_cam(cams, daheng[0], 24, [0, 0, 0])
			cams[0].GainAuto.set(2)
			cams[0].BalanceWhiteAuto.set(2)
			cams[0].TriggerMode.set(1)
			cams[0].TriggerSource.set(0)
			cams[0].LineSelector.set(1)
			cams[0].LineMode.set(1)
			cams[0].LineInverter.set(False)
			cams[0].LineSource.set(2)
			#cams[0].SensorShutterMode.set(2)
			cams[0].UserOutputSelector.set(1)
			#cams[0].UserOutputMode.set(1)
			
			cam_stream_on(cams)

			if debug:
				cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
				cv2.resizeWindow("preview", 500, 300)
			
			print(loop_t, ": successfully initialized daheng camera")		  
			cam_inited = True
			
		except:
			print(traceback.format_exc())
			print(loop_t, ": daheng camera failed to initialized")
			cam_inited = False
			
			if debug:
				print(traceback.format_exc())
	
	if sql_inited and ftp_inited:
	
		# Calibrate daheng camera
		if control[3]:
			
			print(loop_t + ": Starting calibration for daheng")
			
			cams[0].UserOutputValue.set(True)
			cams[0].GainAuto.set(2)
			cams[0].BalanceWhiteAuto.set(2)
						
			for i in range(3):

				while True:
			
					cams[0].TriggerSoftware.send_command()
					images = get_numpyImageBGR(cams)	
					
					if cams[0].GainAuto.get()[0] == 0 and cams[0].BalanceWhiteAuto.get()[0] == 0:
						cams[0].UserOutputValue.set(False)
						sql_inited = set_value(mydb, sql_inited, 'control', 'do_calibration', '0')
						print(loop_t,  ": Daheng calibration completed")
						
						# get required information for logging
						cam_gain = cams[0].Gain.get()
						cams[0].BalanceRatioSelector.set(0)
						cam_red = cams[0].BalanceRatio.get()
						cams[0].BalanceRatioSelector.set(1)
						cam_green = cams[0].BalanceRatio.get()
						cams[0].BalanceRatioSelector.set(2)
						cam_blue = cams[0].BalanceRatio.get()
						
						print("Gain:", cam_gain, "White Balance:", cam_red, cam_green, cam_blue)
						
						break		
		
		# Manually set daheng camera
		if daheng[4]:
			
			cams[0].ExposureTime.set(daheng[0])
			sql_inited = set_value(mydb, sql_inited, 'daheng_camera', 'make_change', '0')
			print(loop_t + ": Manual changes on daheng camera completed")
			print("Exposure: ", cams[0].ExposureTime.get())
									
		# Capture image and preview it
		if cam_inited and debug:
			try:
							
				cams[0].TriggerSoftware.send_command()	
				cams[0].UserOutputValue.set(False)
				images = get_numpyImageBGR(cams)
				
				cv2.imshow("preview", images[0])
				cv2.waitKey(1)
					
			except:
				
				print("Something went wrong with the daheng camera. Reinitializing ...")
				cam_inited = False
				
				if debug:
					print(traceback.format_exc())
		 
		# Save the image via ftp
		if cam_inited and ftp_enable and ftp_inited and control[0] and not daheng[3]:
			
			print(loop_t + ": Starting calibration for daheng")
				
			cams[0].UserOutputValue.set(True)
			cams[0].GainAuto.set(2)
			cams[0].BalanceWhiteAuto.set(2)
						
			for i in range(3):

				while True:
			
					cams[0].TriggerSoftware.send_command()
					images = get_numpyImageBGR(cams)	
					
					if cams[0].GainAuto.get()[0] == 0 and cams[0].BalanceWhiteAuto.get()[0] == 0:
						cams[0].UserOutputValue.set(False)
						sql_inited = set_value(mydb, sql_inited, 'control', 'do_calibration', '0')
						print(loop_t,  ": Daheng calibration completed")
						
						# get required information for logging
						cam_gain = cams[0].Gain.get()
						cams[0].BalanceRatioSelector.set(0)
						cam_red = cams[0].BalanceRatio.get()
						cams[0].BalanceRatioSelector.set(1)
						cam_green = cams[0].BalanceRatio.get()
						cams[0].BalanceRatioSelector.set(2)
						cam_blue = cams[0].BalanceRatio.get()
						
						print("Gain:", cam_gain, "White Balance:", cam_red, cam_green, cam_blue)
						
						break	
							
			cams[0].UserOutputValue.set(True)
			cams[0].TriggerSoftware.send_command()
			images = get_numpyImageBGR(cams)
			cams[0].UserOutputValue.set(False)
			
			# Crop image border
			im_size = images[0].shape
			left_crop = 500
			right_crop = 500
			top_crop = 58
			bottom_crop = 58
			
			images[0] = images[0][top_crop:im_size[0]-bottom_crop,left_crop:im_size[1]-right_crop]

			retval_1, buffer_1 = cv2.imencode(".jpg", images[0])
			flo1 = BytesIO(buffer_1)
			
			sql_inited, image_name = get_value(mydb, sql_inited, 'control', 'image_name')
			
			# camera logging info
			cam_expo = cams[0].ExposureTime.get()
			cam_gain = cams[0].Gain.get()
			cams[0].BalanceRatioSelector.set(0)
			cam_red = cams[0].BalanceRatio.get()
			cams[0].BalanceRatioSelector.set(1)
			cam_green = cams[0].BalanceRatio.get()
			cams[0].BalanceRatioSelector.set(2)
			cam_blue = cams[0].BalanceRatio.get()
			log_info = 'Exposure: ' + str(cam_expo) + '; Gain: ' + str(cam_gain) + '; WB: ' + str(cam_red) + ', ' + str(cam_green) + ', ' + str(cam_blue)

			try:
				ftp.storbinary('STOR daheng/' + image_name, flo1)		
				sql_inited = set_value(mydb, sql_inited, 'daheng_camera', 'capture', '1')
				sql_inited = set_value(mydb, sql_inited, 'daheng_camera', 'log_info', '"' + log_info + '"')
				print(loop_t, ": Done saving daheng image via ftp as", image_name)
				print(log_info)
			
			except:
			
				print(loop_t, ": Unable to save daheng image via ftp, resort to local save")
				cv2.imwrite("/home/ailand/Pictures/daheng/" + loop_t + ".jpg", images[0])
				ftp_inited = False
			
				if debug:
					print(traceback.format_exc())
