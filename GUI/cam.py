# version:1.0.1905.9051# works really slow (video drops to <= 20 FPS)
from cameraSetup import *
from exifOperations import *

#import sys
#print(sys.path)

"""NOTE1
Basic scripts to access and display the Daheng cameras, adapted from the examples
camera initializing can/should be done by setupFile.txt
for reliable use (independent of USB port) accessing the cameras by serial number is better 
(has to be determined by hand before)
"""#NOTE1
def getCams():
    device_manager = get_deviceManagerGX()
    cams = []
    cams = get_cams_byIndex(device_manager, cams)

    return device_manager, cams


def cam(device_manager, cams, exposureTime):

    # cams =  get_cams_bySerial(device_manager, cams, cams_sn)
    init_cam(cams, exposureTime, 24.0, [0.0, 0.0, 0.0])  # automatically fills in the array cams could be augmented to support load in by file

    for i in range(len(cams)):
        cams[i].TriggerMode.set(1)
        cams[i].TriggerSource.set(0)
        cams[i].LineSelector.set(1)
        cams[i].LineMode.set(1)
        cams[i].LineInverter.set(True)
        cams[i].LineSource.set(1)

    # print(cams[0].DeviceLinkCurrentThroughput.get_range())
    # print(cams[0].DeviceLinkCurrentThroughput.get())
    visualise = True
    fps = True
    capture_image_press = True
    capture_image_timed = 100   # time increment with which to take images in ms

    #cam_stream_on(cams)

    #streamToWindow(cams, device_manager, fps, capture_image_press, capture_image_timed, visualise)
    # print_deviceInfo(device_manager)
