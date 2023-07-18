import cv2
import numpy as np

import gxipy as gx
import time

from datetime import datetime  # for filenames and multiple images per second
import os


def get_deviceManagerGX():
    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num == 0:
        print("Number of enumerated devices is 0, no camera detected")
        return 0
    return device_manager


def print_deviceInfo(device_manager):
    dev_num, dev_info_list = device_manager.update_device_list()
    print(dev_info_list)


def get_cams_byIndex(device_manager, cams):
    dev_num, dev_info_list = device_manager.update_device_list()
    for i in range(dev_num):
        cams.append(device_manager.open_device_by_index(i + 1))
    return cams


def get_cams_bySerial(device_manager, cams, cams_sn):
    dev_num, dev_info_list = device_manager.update_device_list()
    if len(cams_sn) != dev_num:
        print("Dimension miss match! Number of Cameras is not number of serial numbers provided")
        return 0
    for i in range(dev_num):
        cams.append(device_manager.open_device_by_sn(cams_sn[i - 1]))
    return cams


def init_cam(cams, exposure=0, gain=0, white=[0, 0, 0]):
    # should be simplified via call to an external setup file, which should be accessible/changeable via a GUI cf. todo
    """
    Initialize camera(s)
        cams: camera, can be single or a list
        exposure: exposure time. If no value is given, the exposure will be chosen automatically
        gain: amplification of signal. If no value is given, the gain will be chosen automatically
        white: white balance modifications, zero will default to auto
    """
    for i, cam in enumerate(cams):
        # set continuous acquisition
        cam.TriggerMode.set(gx.GxSwitchEntry.OFF)  # Not explained what this does yet
        # turn off the limitation of acquisition bit rate --> was a bottleneck before, min max values
        cam.DeviceLinkThroughputLimitMode.set(gx.GxSwitchEntry.OFF)
        # white balance
        if cam.PixelColorFilter.is_implemented():
            if white == [0, 0, 0]:
                cam.BalanceWhiteAuto.set(gx.GxAutoEntry.CONTINUOUS)
            else:  # needs to be determined for every camera according to light conditions, should only be used with controlled lighting
                # select RGB channel to set balance 0=R 1=G 2=B
                cam.BalanceWhiteAuto.set(gx.GxAutoEntry.OFF)
                cam.BalanceRatioSelector.set(0)
                cam.BalanceRatio.set(white[0])
                cam.BalanceRatioSelector.set(1)
                cam.BalanceRatio.set(white[1])
                cam.BalanceRatioSelector.set(2)
                cam.BalanceRatio.set(white[2])
        # set gain
        if gain == 0:
            cam.GainAuto.set(gx.GxAutoEntry.CONTINUOUS)
        else:
            cam.GainAuto.set(gx.GxAutoEntry.OFF)
            cam.Gain.set(gain)
        # set exposure
        if exposure == 0:
            cam.AutoExposureTimeMin.set(2000)
            cam.AutoExposureTimeMax.set(2000)
            cam.ExposureAuto.set(gx.GxAutoEntry.CONTINUOUS)
        else:
            cam.ExposureAuto.set(gx.GxAutoEntry.OFF)
            # cam.ExposureTime.set(gx.GxAutoEntry.ONCE)
            cam.ExposureTime.set(exposure)
        cams[i] = cam
    return cams


def cam_stream_on(cams):
    for i in range(len(cams)):
        cams[i].stream_on()


def cam_stream_off(cams):
    for i in range(len(cams)):
        cams[i].stream_off()


def cam_terminate(cams):
    for i in range(len(cams)):
        cams[i].close_device()


def get_numpyImageRGB(cams):
    numpy_images = []
    for cam in cams:
        raw_image = cam.data_stream[0].get_image()  # Use the camera to capture a picture
        rgb_image = raw_image.convert("RGB")  # Get the RGB image from the color original image
        numpy_image = rgb_image.get_numpy_array()  # Create numpy array from RGB image data
        if rgb_image is None:
            print("rgb_image is empty")
            return None
        numpy_images.append(numpy_image)
    return numpy_images


def activate_trigger(cams):
    for cam in cams:
        cam.TriggerSoftware.send_command()


def get_numpyImageBGR(cams):
    numpy_images = []
    for cam in cams:  # not understood yet why the i is necessary,
        cam.TriggerSoftware.send_command()
        raw_image = cam.data_stream[0].get_image()  # Use the camera to capture a picture
        if raw_image is None:
            numpy_image_bgr = raw_image
        else:
            rgb_image = raw_image.convert("RGB")  # Get the RGB image from the color original image
            numpy_image_rgb = rgb_image.get_numpy_array()  # Create numpy array from RGB image data
            numpy_image_bgr = cv2.cvtColor(numpy_image_rgb,
                                           cv2.COLOR_RGB2BGR)  # opencv uses BGR images, and converts RGB to BGR
        numpy_images.append(numpy_image_bgr)
    return numpy_images


def get_frame_rate(prev_frame_time, i=0):
    # https://www.geeksforgeeks.org/python-displaying-real-time-fps-at-which-webcam-video-file-is-processed-using-opencv/
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time[i])
    prev_frame_time[i] = new_frame_time
    fps = int(fps)
    return fps, prev_frame_time


def get_constant_framerate(current_fps, time_gap, constant_fps=0, i=0):
    new_time = time.time()
    dif = new_time - time_gap[i]
    if dif > 0.5:
        time_gap[i] = new_time
        constant_fps = current_fps
    return constant_fps, time_gap


def get_exposuretime(cam):
    return cam.ExposureTime.get()


def set_exposuretime(value, cam):
    return cam.ExposureTime.set(value)


def set_gain(value, cam):
    return cam.Gain.set(value)


def streamToWindow(cams, device_manager, fps=False, capture_image_press=False, capture_image_timed=0.0,
                   visualize=False):
    """
    Stream camera feed into external windows. Press a to capture and esc to close
    cams: camera, can be single or a list
    """

    # save images at will to output folder nested in cwd
    output_folder = 'output'

    # adjust resolution of image
    resolution_factor = 1.0
    fontsize = round(resolution_factor * 5 + 0.5)
    fontLineWidth = round(resolution_factor * 3 + 0.5)
    # fps output
    prev_frame_time = np.zeros(len(cams))  # used as fps counter for each cam
    time_gap = np.zeros(len(cams))  # used to only update the frame rate every 500ms or so
    constant_fps = 0
    # capture images with increment
    elapsed_image_time = time.time()
    for i, cam in enumerate(cams):
        win_name = device_manager.get_device_info()[i]["model_name"]
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)  # Create a window named camera xxxxx

    # start data acquisition
    cam_stream_on(cams)

    while True:
        # images = get_numpyImageRGB(cams)
        images = get_numpyImageBGR(cams)
        for i, cam in enumerate(cams):
            # setting up the frame
            win_name = device_manager.get_device_info()[i]["model_name"]
            if fps:
                # setting up fps counter with update
                fps, prev_frame_time = get_frame_rate(prev_frame_time, i)  # returns int
                fps = str(fps)
                # updating fps every 500ms or so to display
                constant_fps, time_gap = get_constant_framerate(fps, time_gap, constant_fps, i)

                # needs to be added in order to display the frame rate
                font = cv2.FONT_HERSHEY_COMPLEX  # any font is viable for ease of use
                cv2.putText(images[i], constant_fps, (100, 100), font, fontsize, (0, 0, 255), fontLineWidth,
                            cv2.LINE_AA)
            if visualize:
                # Display the captured image in the video window
                cv2.imshow(win_name, images[i])

            # save images at will to output folder here ~/currentDirectory/output/
            if capture_image_press:
                path = os.getcwd()
                os.makedirs(output_folder, exist_ok=True)
                if cv2.waitKey(1) & 0xFF == 32:
                    for j, c in enumerate(cams):
                        picturename = path + '/output/' + device_manager.get_device_info()[j][
                            "model_name"] + "_" + datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3] + '.jpg'
                        cv2.imwrite(picturename, images[j])
            if capture_image_timed:
                path = os.getcwd()
                os.makedirs(output_folder, exist_ok=True)
                if time.time() - elapsed_image_time > capture_image_timed/1000.0:
                    print('before: ', datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3])
                    for j, c in enumerate(cams):
                        picturename = path + '/' + output_folder + '/' + device_manager.get_device_info()[j][
                            "model_name"] + "_" + datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3] + '.jpg'
                        cv2.imwrite(picturename, images[j])
                    print('after: ', datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3])
                    elapsed_image_time = time.time()
        # Press esc to exit the program
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam_stream_off(cams)
    cam_terminate(cams)
