# Version 1.1.1
## dahengCamera.py
- set the gain to 0 (manual)
- remove gain auto once during initialization and calibration
## cameraSetup.py
- for the init_cam function, setting 0 for exposure, gain, white balance will result in automatic mode. For automatic mode use none instead

# Version 1.1.0
## startArducam.sh
- change prefix for all file to '/home/ailand/handwagon_software/raspberry_pi_4/Handwagon/'
## dahengCamera.py
- change from manual strobing to auto strobing from camera