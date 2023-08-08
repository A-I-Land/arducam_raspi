# This Python file uses the following encoding: utf-8
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from datetime import datetime
from cameraSetup import *
from database import *
from log import *
from data import *
from func_timeout import func_timeout, FunctionTimedOut
import time
import qimage2ndarray
import cv2 # OpenCV
import sys
import numpy as np
import gxipy as gx
import os

Path_Restart_Mysql = "/home/ailand/GUI_Data/mysql/restart_mysql.sh.x"
Path_Images = "GUI_Data/output/"

def getStream(images, device_manager, cams, fps, i):
    """
    Setzt die Frame Rate in die Bilder des Streams und gibt diese zurück
    """
    resolution_factor = 1.0
    font = cv2.FONT_HERSHEY_COMPLEX
    fontsize = round(resolution_factor * 5 + 0.5)
    fontLineWidth = round(resolution_factor * 3 + 0.5)

    if fps:
        # needs to be added in order to display the frame rate
        font = cv2.FONT_HERSHEY_COMPLEX  # any font is viable for ease of use
        cv2.putText(images[i], fps, (100, 100), font, fontsize, (0, 0, 255), fontLineWidth,
                    cv2.LINE_AA)

    return images[i]

def make_Images(cams, labelNum, num, interval, labelImage, labelImage2, img_Names, imgInfo, labelCountdown, cameraStatus, buttonBreak, GPSLng, GPSLat, imgData, tableDatasets, datasetsData):
    """
    Macht in einem vorgegeneben abstand automatisch Bilder und gibt diese zurück
    """
    loop = 0

    while loop < num:
        labelCountdown.setText("-" + str(interval) + "-")
        i = interval
        while i > 0:
            labelCountdown.setText("-" + str(i - 1) + "-")
            time.sleep(1)
            i = i - 1
            while buttonBreak.isHidden():
                time.sleep(1)
        #lng = 0
        #lat = 0
        try:
           lng, lat = func_timeout(2,getGPSData, args=())
        except:
            eMessage = "No GPS Connection!!!"
            print(eMessage)
            writeLog("Error", eMessage)
            lng = 0
            lat = 0

        GPSLng.append(lng)
        GPSLat.append(lat)
        img_Names, imgData = make_Image(cams, labelNum, labelImage, labelImage2, img_Names, imgInfo, cameraStatus, imgData, tableDatasets, datasetsData)
        loop = loop + 1

    return img_Names, imgData, GPSLng, GPSLat


def setCameraData(table, setting, value):
    """
    Setzt den übergebenen Wert in der mysql Tabelle
    """
    try:
       func_timeout(2,setDatabaseData, args=(table, setting, value))
       #getLockStatus(table)
    except:
        eMessage = "Connection to Sql failed!!! Please check cable connection!"
        print(eMessage)
        writeLog("Error", eMessage)
        try:
            os.system(Path_Restart_Mysql)
        except Exception as e:
            eMessage = "Restarting SQL failed: try restarting the GUI or the Surface \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)


def getCameraData(table, setting):
    """
    Gibt die Informationen der übergebenen mysql Tabelle zurück
    """
    try:
        value = func_timeout(2,getDatabaseData, args=(table, setting))
    except:
        eMessage = "Connection to Sql failed!!! Please check cable connection!"
        print(eMessage)
        writeLog("Error", eMessage)
        value = ""
        try:
            os.system(Path_Restart_Mysql)
        except Exception as e:
            eMessage = "Restarting SQL failed: try restarting the GUI or the Surface \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    return value

def make_Image(cams, labelNum, labelImage, labelImage2, img_Names, imgInfo, cameraStatus, imgData, tableDatasets, datasetsData):
    """
    Bild wird aufgenommen und zurückgegeben
    """

    textNum = labelNum.text().split(" ")
    num = int(textNum[1])
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    textField = deleteSpaces(imgInfo[0])


    picturePath = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f') + "_" +  textField + "_" + imgInfo[1] + "_" + imgInfo[2] + "_" "Kamera2"
    picturename = picturePath + ".jpg"
    setCameraData("control", "image_name", picturename)
    setCameraData("control", "soft_capture", "1")
    #print("time1 start")
    time.sleep(1)

    sec = 0
    noSuccess = True

    while noSuccess and sec <= 4:
        try:
            img = cv2.imread("/home/ailand/daheng/" + picturename)
            cv2.imwrite(Path_Images + picturename ,img)
            labelNum.setText("Bilder: " + str(num + 1) + " / " + textNum[3])
            img_Name = output_folder + "/" + picturePath
            img_Names.append(img_Name)
            updateTable(tableDatasets, 5, str(num + 1) + " / " + textNum[3], datasetsData)
            noSuccess = False
        except Exception as e:
            eMessage = "Could not read Image \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
            #labelImage.setText("Bild konnte nicht gespeichert werden !!!!")
            #noSuccess = True
            sec = sec + 1
            time.sleep(1)

    #print("time2")
    try:
        #img = cv2.imread("GUI/output/" + picturename)
        #img = resizeImg(img, (1100,500))
        img = cv2.resize(img, (535,500))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = qimage2ndarray.array2qimage(img)
        labelImage.setPixmap(QPixmap.fromImage(img))
    except Exception as e:
        eMessage = "Could not display image \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
        #labelImage.setText("Bild konnte nicht ausgegeben werden !!!!")


    if noSuccess == False:
        try:
            numdataset = len(datasetsData) - 1
            id = datasetsData[numdataset][0]
            changeDatabaseDataset("Images", img_Names, "array", id)
            #print("Number: " + str(num))
            imageNum = str(num + 1) + " / " + textNum[3]
            changeDatabaseDataset("ImageNum", imageNum, "text", id)
            addDatabaseImage(img_Name)

        except Exception as e:
            eMessage = "Could not save image to Database \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    writeLog("image", "")
    imgInfo = getCameraData("daheng_camera", "log_info")
    imgData.append(imgInfo)
    writeLog("imageInfo", imgInfo)

    #print("time3")

    return img_Names, imgData

def resizeImg(image, dim):
    """
    Größe des übergebenen Bilders wird enstprechend der übergebenen Dimension angepasst
    """

    img = cv2.resize(image, dim)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = img.shape
    bytesPerLine = ch * w
    img = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
    #img = qimage2ndarray.array2qimage(img)
    return img


def get_Image(cams):
    """
    Aktuelle Frame der Kamera wird entnommen und als Bild zurückgegeben
    """

    numpy_images = []
    try:
        for cam in cams:  # not understood yet why the i is necessary,
            activate_trigger(cams)
            raw_image = cam.data_stream[0].get_image()  # Use the camera to capture a picture
            if raw_image is None:
                numpy_image_bgr = raw_image
            else:
                rgb_image = raw_image.convert("RGB")  # Get the RGB image from the color original image
                numpy_image_rgb = rgb_image.get_numpy_array()  # Create numpy array from RGB image data
                numpy_image_bgr = cv2.cvtColor(numpy_image_rgb,
                                             cv2.COLOR_RGB2BGR)  # opencv uses BGR images, and converts RGB to BGR
            numpy_images.append(numpy_image_bgr)
    except Exception as e:
        eMessage = "Getting Image from Daheng Camera Failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
    return numpy_images

def deleteSpaces(text):
    """
    Alle Leerzeichen des übergebenen Textes werden entfernt
    """

    splitText = text.split(" ")
    newText = ""

    for i in splitText:
        newText = newText + i

    return newText



