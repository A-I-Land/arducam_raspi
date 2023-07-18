# capturing images and writing some example exif data for Bayer
from cameraSetup import *
from exifOperations import *

def streamToWindow_Exif(cams, device_manager, fps=False, capture_image_press=False, capture_image_timed=0.0,
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
                cv2.putText(images[i], constant_fps, (200, 300), font, fontsize, (0, 0, 255), fontLineWidth,
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
                        # NOTE EXIF
                        write_exif(picturename, cams[j])
                        # NOTE EXIF END
            if capture_image_timed:
                path = os.getcwd()
                os.makedirs(output_folder, exist_ok=True)
                if time.time() - elapsed_image_time > capture_image_timed/1000.0:
                    # print('before: ', datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3])
                    for j, c in enumerate(cams):
                        picturename = path + '/' + output_folder + '/' + device_manager.get_device_info()[j][
                            "model_name"] + "_" + datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3] + '.jpg'
                        cv2.imwrite(picturename, images[j])
                    # print('before: ', datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3])
                    write_exif(picturename, cams[j])
                    # print('after: ', datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3])
                    elapsed_image_time = time.time()
        # Press esc to exit the program
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam_stream_off(cams)
    cam_terminate(cams)

def write_exif(path, cam):
    image = Image.open(path)
    exif_data = image.getexif()
    date = path[-23:-15]
    time = path[-14:-8]
    my_dict = {'ImageWidth': 200, 'Model': 'MER2', 'Make': 'Daheng', 'DateTimeOriginal': date+' '+time, 'ImageDescription': 'Some description', 'ExposureTime': get_exposuretime(cam)}
    pil_write_dict_exif(exif_data, my_dict)
    # print(my_dict)
    image.save(path, exif=exif_data)
    image.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    device_manager = get_deviceManagerGX()
    cams = []
    cams = get_cams_byIndex(device_manager, cams)
    # cams =  get_cams_bySerial(device_manager, cams, cams_sn)
    init_cam(cams, 2500.0, 24.0,
             [0.0, 0.0, 0.0])  # automatically fills in the array cams could be augmented to support load in by file
    # print(cams[0].DeviceLinkCurrentThroughput.get_range())
    # print(cams[0].DeviceLinkCurrentThroughput.get())
    visualise = True
    fps = True
    capture_image_press = True
    capture_image_timed = 1  # time increment with which to take images in ms

    streamToWindow_Exif(cams, device_manager, fps, capture_image_press, capture_image_timed, visualise)
    # print_deviceInfo(device_manager)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
