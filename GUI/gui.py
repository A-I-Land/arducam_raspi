import sys
import cv2
import imutils
import webbrowser
import mysql.connector
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PinCode import *
from threading import Timer
from datetime import datetime
from datetime import timedelta
from time import time
from camera import *
from data import *
from log import *
from database import *
from settings import *
from sendEmail import *
from DataRecovery import *
from func_timeout import func_timeout, FunctionTimedOut
import cv2
import qimage2ndarray
import psutil
import os
import gxipy as gx
from cam import *
from cameraSetup import *
from zoom import *
from InfoWindow import *
from UploadWindow import *

CULTIVATION = ["", "Weizen", "Gerste", "Raps", "Mais", "Zuckerrübe", "Kartoffel", "Soja", "Sonnenblume", "Stoppel", "Grünland", "Erbse", "Ackerbohne", "Boden"]
LIGHT = ["", "sonnig", "bewölkt", "dämmrig", "dunkel"]
BBCH = ["", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "22", "23", "24", "25", "29", "31", "32", "35", "39"]
GROUND = ["", "trocken", "feucht"]
TRIGGER = ["manuell", "automatisch"]
INTERVAL = ["1 sek.", "2 sek.", "3 sek.", "4 sek.", "5 sek.", "6 sek.", "7 sek.", "8 sek.", "9 sek.", "10 sek."]
LANGUAGE = ["Deutsch"]
DEVICE = ["Handgerät 1", "Handgerät 2", "Handgerät 3", "Handgerät 4", "Handgerät 5", "Handgerät 6"]
SENSORBOX = ["Sensorbox 1", "Sensorbox 2", "Sensorbox 3", "Sensorbox 4", "Sensorbox 5", "Sensorbox 6"]
UPLOAD = ["Mobile Daten", "Wlan"]
CAMERA = ["ON"]
SERVER = ["QA", "PROD"]
DATASET = ['Datum', 'Kultur', 'BBCH', 'Licht', 'Boden', 'Anzahl \n Bilder', 'Hochgeladen', 'Auswahl']
LOGS = ['Datum', 'LogFile', 'Auswahl', 'Öffnen']
INFLUENCES = ["", "Schäden an der Kulturpflanze (bspw: Hagel, Fraß, mechanisch)", "Blattverfärbung (bspw: Mangel, Frost)", "Hitzestress", "Wasserschaden", "Phytotox (doppelt appliziert am Vorgewende)", "Herbizidschaden (Rückstände im Tank)"]
INFESTATION = ["", "Distelnest", "starke Verunkrautung", "keine Verunkrautung"]

Growth_Height_Default = "1"
Image_Max_Deafault = 5
Exposure_Time_Default = 240
Dataset_Email_Days = 7
GUI_Version = "Version: 2.1.6"
Email_Receiver_Logs = "kuehnast@a-i.land"
Email_Receiver_DataNum = "kuehnast@a-i.land"
#PIN = 1234

Path_GUI_Icon = "/home/ailand/GUI_Data/plant.png"
Path_Daheng_Preview = "/home/ailand/daheng/preview.jpg"
Path_Log_Files = "/home/ailand/GUI_Data/logs/"
Path_Images = "GUI_Data/"


class test(QWidget):
    def __init__(self):
      super(test, self).__init__()

      self.textFont2 = QFont()
      self.textFont2.setPointSize(11)
      self.textFont2.setBold(True)

      self.textFontZoom = QFont()
      self.textFontZoom.setPointSize(20)
      self.textFontZoom.setBold(True)

      self.labelLed = QLabel("LED")
      self.labelLed.setStyleSheet("background-color: green; color: white")
      self.labelLed.setAlignment(Qt.AlignCenter)
      self.labelCam1 = QLabel("Cam 1")
      self.labelCam1.setStyleSheet("background-color: green; color: white")
      self.labelCam1.setAlignment(Qt.AlignCenter)
      self.labelCam2 = QLabel("Cam 2")
      self.labelCam2.setStyleSheet("background-color: green; color: white")
      self.labelCam2.setAlignment(Qt.AlignCenter)
      labelSettings = QLabel("Einstellungen:")
      labelSettings.setFont(self.textFont2)
      labelVersion = QLabel(GUI_Version)
      self.labelBattery = QLabel()
      now = QDateTime.currentDateTime()
      self.labelTime = QLabel(now.toString())
      self.buttonCamera = QPushButton("Kamera")
      self.buttonCamera.setFont(self.textFont2)
      self.buttonCamera.setStyleSheet("height: 70")
      self.buttonCamera.clicked.connect(lambda:
      self.Stack.setCurrentIndex(1))
      self.buttonLogs = QPushButton("Logs")
      self.buttonLogs.setFont(self.textFont2)
      self.buttonLogs.setStyleSheet("height: 70")
      self.buttonLogs.clicked.connect(lambda:
      self.Stack.setCurrentIndex(2))
      self.buttonAdmin = QPushButton("Admin")
      self.buttonAdmin.setStyleSheet("height: 70")
      self.buttonAdmin.setFont(self.textFont2)
      self.buttonAdmin.clicked.connect(lambda:
      self.Stack.setCurrentIndex(5))
      self.buttonFokus = QPushButton("Fokus")
      self.buttonFokus.setStyleSheet("height: 70")
      self.buttonFokus.setFont(self.textFont2)
      self.buttonFokus.clicked.connect(lambda:
      self.Stack.setCurrentIndex(10))
      self.buttonDataset = QPushButton("Datensatz")
      self.buttonDataset.setStyleSheet("height: 70")
      self.buttonDataset.setFont(self.textFont2)
      self.buttonDataset.pressed.connect(self.openDatasetWidget)
      self.buttonDataset.setHidden(True)


      self.stack1 = QWidget()
      self.stack2 = QWidget()
      self.stack3 = QWidget()
      self.stack4 = QWidget()
      self.stack5 = QWidget()
      self.stack6 = QWidget()
      self.stack7 = QWidget()
      self.stack8 = QWidget()
      self.stack9 = QWidget()
      self.stack10 = QWidget()
      self.stack11 = QWidget()

      try:
        self.logfiles = readLogs()
      except Exception as e:
        print("Reading Log Information failed \n" + str(e))
        self.logfiles = []

      try:
        self.datasets = readDatasetData()
      except Exception as e:
        eMessage = "Reading Dataset Information failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
        self.datasets = []

      """
      try:
        writeDatasetData(self.datasets)
      except Exception as e:
        eMessage = "Writing Dataset Information failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
      """

      deleteOldDatasets(self.datasets)

      self.textIsSet = [False, False, False, False, False, False]
      self.cameraStatus = [True, True]
      self.lastPage = 0
      self.currentPage = 0
      self.settingsDataset = [CULTIVATION[0], LIGHT[0], BBCH[0], GROUND[0], Growth_Height_Default, "", "", ""]
      self.maxImages = Image_Max_Deafault
      self.statusImageThread = True
      self.autoImages = False
      self.imageZoom = 1
      self.infoWindow = None
      self.datasetNum = 0
      self.imagesNum = 0
      self.datasetsDate = None
      self.GuiOn = True
      self.imagesBlurred = False

      self.uploadWindow = None
      #self.uploadWindow.setErrorMessage("test")
      #self.uploadWindow.show()

      try:
        self.datasetNum, self.imagesNum, self.datasetsDate = readDatasetNum()
      except Exception as e:
        eMessage = "Reading Dataset Number failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
        self.datasetNum = 0
        self.imagesNum = 0
        self.datasetsDate = datetime.now()
        self.datasetsDate = self.datasetsDate.strftime('%a. %b %d %X %Y')

      #print("DateTime: " + self.datasetsDate)

      oldDate = datetime.strptime(self.datasetsDate, '%a. %b %d %X %Y')
      timeNow = datetime.now() - oldDate
      #print("NewTime: " + str(timeNow))

      try:
        self.settingAdmin = readAdminSettings()
        self.maxImages = self.settingAdmin[6]
      except Exception as e:
        eMessage = "Reading Admin Settings failed \n" + str(e)
        print(eMessage)
        self.maxImages = Image_Max_Deafault
        writeLog("Error", eMessage)
        self.settingAdmin = [LANGUAGE[0], DEVICE[0], SENSORBOX[0], UPLOAD[0], CAMERA[0], CAMERA[0],str(Image_Max_Deafault), SERVER[0]]

      try:
        self.settingsCamera = readCamSettings()
      except Exception as e:
        eMessage = "Reading Camera Settings failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
        self.settingsCamera = [TRIGGER[0], INTERVAL[0], str(Exposure_Time_Default), str(Exposure_Time_Default)]

      self.checkBoxCheckedNum = 0
      self.checkBoxUploadedNum = 0

      try:
        self.pinKey, self.pinSalt = readPinCode()
      except Exception as e:
        eMessage = "Reading Pin Code Information failed  \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)


      self.textFont = QFont()
      self.textFont.setPointSize(13)
      self.textFont.setBold(True)
      self.ButtonFont = QFont()
      self.ButtonFont.setPointSize(13)
      self.ButtonFont.setBold(True)
      #setCameraData()


      self.start()
      self.camera()
      self.logs()
      self.newDataset()
      self.recording()
      self.adminCheck()
      self.adminSettings()
      self.query()
      self.cameraCalib()
      self.queryDelete()
      self.fokusPage()

      self.Stack = QStackedWidget (self)
      self.Stack.addWidget (self.stack1)
      self.Stack.addWidget (self.stack2)
      self.Stack.addWidget (self.stack3)
      self.Stack.addWidget (self.stack4)
      self.Stack.addWidget (self.stack5)
      self.Stack.addWidget (self.stack6)
      self.Stack.addWidget (self.stack7)
      self.Stack.addWidget (self.stack8)
      self.Stack.addWidget (self.stack9)
      self.Stack.addWidget (self.stack10)
      self.Stack.addWidget (self.stack11)
      self.Stack.currentChanged.connect(self.pageChanged)

      self.recordingStart = False
      self.imgMaking = False
      self.cams = None
      self.deviceManager = None
      self.imageNames = []
      self.imageData = []
      self.GPSLng = []
      self.GPSLat = []
      self.datasetNames = []
      self.uploadResponse = ""
      self.uploadStatus = False
      self.enteredASettings = False
      self.fokusImage = None

      if timeNow.days >= Dataset_Email_Days:
          tEmail = Timer(0, self.sendDatasetNum, args=())
          tEmail.start()


      t = Timer(1.0, self.updateTime, args=())
      t.start()
      tTrigger = Timer(0.5, self.getTrigger, args=())
      tTrigger.start()
      tCamStatus = Timer(0.5, self.getCamStatus, args=())
      tCamStatus.start()


      hbox = QGridLayout(self)
      hbox.addWidget(self.labelTime,0,0)
      hbox.addWidget(labelVersion,0,2)
      #hbox.addWidget(self.labelBattery,0,1)
      #hbox.addWidget(self.labelLed,0,3)
      hbox.addWidget(self.labelCam1,0,4)
      hbox.addWidget(self.labelCam2,0,5)
      hbox.addWidget(self.Stack, 1,0,1,6)
      hbox.addWidget(labelSettings, 2,0)
      hbox.addWidget(self.buttonCamera, 2,1)
      hbox.addWidget(self.buttonLogs, 2,2)
      hbox.addWidget(self.buttonAdmin, 2,3)
      hbox.addWidget(self.buttonFokus, 2,4)
      hbox.addWidget(self.buttonDataset, 2,5)

      try:
        self.start_camera()
      except Exception as e:
        eMessage = "Starting Camera Failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

      try:
        status, INames, IData, Lat, Lng, setting, datData = readRecoveryDataset()
      except Exception as e:
        eMessage = "Getting Last Dataset Information failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
        status = False
      if status:
          self.imageNames = INames
          self.imageData = IData
          self.GPSLat = Lat
          self.GPSLng = Lng
          self.settingsCamera = setting
          self.settingsDataset = datData
          self.recoverRecording()

      self.setAdminSettings()
      self.setCameraSettings()
      self.setLayout(hbox)
      self.setGeometry(100, 60, 800,500)
      #self.setWindowTitle('StackedWidget demo')
      self.show()

    def start(self):
        """
        Startseite
        """

        layout = QGridLayout()
        labelHeadline1 = QLabel("Neuen Datensatz anlegen")
        labelHeadline1.setFont(self.textFont)
        layout.addWidget(labelHeadline1, 0,0)
        labelHeadline2 = QLabel("Bisherige Datensätze:")
        labelHeadline2.setFont(self.textFont)
        layout.addWidget(labelHeadline2, 1,0)

        self.labelNoticeUpload = QLabel("Datensatz wird hochgeladen")
        self.labelNoticeUpload.setStyleSheet("background-color: blue; color: white")
        self.labelNoticeUpload.setAlignment(Qt.AlignCenter)
        self.labelNoticeUpload.hide()
        layout.addWidget(self.labelNoticeUpload, 1,1)

        #data = readData()

        buttonDataset = QPushButton("Datensatz starten")
        buttonDataset.setStyleSheet("background-color: green; height: 100; text-align: center; color: white")
        buttonDataset.setFont(self.ButtonFont)
        #buttonDataset.pressed.connect(self.show_new_window)
        buttonDataset.clicked.connect(lambda:
        self.Stack.setCurrentIndex(3))
        layout.addWidget(buttonDataset, 0,1)

        self.tableDatasets = QTableWidget()
        self.tableDatasets.setStyleSheet('QAbstractItemView::indicator {width: 200px; height: 80px;}');
        self.tableDatasets.setColumnCount(8)
        self.tableDatasets.setHorizontalHeaderLabels(DATASET)
        header = self.tableDatasets.horizontalHeader()
        self.tableDatasets.setColumnWidth(0,250)
        self.tableDatasets.setColumnWidth(5,10)
        self.tableDatasets.setColumnWidth(7,180)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        #tableDatasets.data = DATASETS
        #tableDatasets.setData()

        #tableDatasets.insertRow(0);
        setData(self.tableDatasets, self.datasets)
        self.tableDatasets.cellChanged.connect(self.checkBoxChanged)
        #tableDatasets.setItem(0,0,item)
        layout.addWidget(self.tableDatasets, 2,0,1,2)

        self.buttonDeleteST = QPushButton("Ausgewählte Datensätze löschen")
        #self.buttonDeleteST.pressed.connect(self.deleteSelectedDataset)
        self.buttonDeleteST.clicked.connect(lambda:
        self.Stack.setCurrentIndex(9))
        self.buttonDeleteST.setFont(self.ButtonFont)
        self.buttonDeleteST.setStyleSheet("background-color: red; height: 100; color: white")
        layout.addWidget(self.buttonDeleteST, 3,0)

        self.buttonUpload = QPushButton("UPLOAD ausgewählter Datensätze")
        self.buttonUpload.pressed.connect(self.startUploadThread)
        self.buttonUpload.setFont(self.ButtonFont)
        self.buttonUpload.setStyleSheet("background-color: green; height: 100; color: white")
        layout.addWidget(self.buttonUpload, 3,1)

        self.stack1.setLayout(layout)

    def camera(self):
        """
        Kamera Einstellungen
        """

        layout = QGridLayout()
        labelHeadline = QLabel("Einstellungen: Kamera")
        labelHeadline.setFont(self.textFont)
        layout.addWidget(labelHeadline, 0,0,1,2)

        labelTrigger = QLabel("Auslöser:")
        labelTrigger.setFont(self.textFont)
        layout.addWidget(labelTrigger, 1,0)
        self.comboBoxTrigger = QComboBox()
        self.comboBoxTrigger.setStyleSheet("height: 100")
        self.comboBoxTrigger.setFont(self.textFont)
        self.comboBoxTrigger.addItems(TRIGGER)
        self.comboBoxTrigger.currentTextChanged.connect(self.checkTriggerChange)
        layout.addWidget(self.comboBoxTrigger, 1,1,1,3)

        labelInterval = QLabel("Bild alle:")
        labelInterval.setFont(self.textFont)
        layout.addWidget(labelInterval, 2,0)
        self.comboBoxInterval = QComboBox()
        self.comboBoxInterval.setStyleSheet("height: 100")
        self.comboBoxInterval.setFont(self.textFont)
        self.comboBoxInterval.addItems(INTERVAL)
        self.comboBoxInterval.setEnabled(False)
        layout.addWidget(self.comboBoxInterval, 2,1,1,3)

        labelLightTime1 = QLabel("Belichtungszeit Kamera 1 (µs):")
        labelLightTime1.setFont(self.textFont)
        layout.addWidget(labelLightTime1, 3,0,1,3)
        buttonLightplus1 = QPushButton("+")
        buttonLightplus1.setStyleSheet("height: 100")
        buttonLightplus1.setFont(self.textFont)
        buttonLightplus1.clicked.connect(lambda: self.increaseExposure(self.textBoxLightTime1))
        layout.addWidget(buttonLightplus1, 4,3)
        labelDark1 = QLabel("dunkel")
        labelDark1.setFont(self.textFont)
        labelDark1.setAlignment(Qt.AlignCenter)
        layout.addWidget(labelDark1, 5,3)
        self.textBoxLightTime1 = QLineEdit()
        self.textBoxLightTime1.setStyleSheet("height: 100")
        self.textBoxLightTime1.setFont(self.textFont)
        self.textBoxLightTime1.setAlignment(Qt.AlignCenter)
        self.textBoxLightTime1.setText(str(Exposure_Time_Default))
        layout.addWidget(self.textBoxLightTime1, 4,1,1,2)
        buttonLightminus1 = QPushButton("-")
        buttonLightminus1.setStyleSheet("height: 100")
        buttonLightminus1.setFont(self.textFont)
        buttonLightminus1.clicked.connect(lambda: self.decreaseExposure(self.textBoxLightTime1))
        layout.addWidget(buttonLightminus1, 4,0)
        labelSunny1 = QLabel("sonnig")
        labelSunny1.setFont(self.textFont)
        labelSunny1.setAlignment(Qt.AlignCenter)
        layout.addWidget(labelSunny1, 5,0)

        labelLightTime2 = QLabel("Belichtungszeit Kamera 2 (µs):")
        labelLightTime2.setFont(self.textFont)
        #layout.addWidget(labelLightTime2, 5,0,1,3)
        buttonLightplus2 = QPushButton("+")
        buttonLightplus2.setStyleSheet("height: 100")
        buttonLightplus2.setFont(self.textFont)
        buttonLightplus2.clicked.connect(lambda: self.increaseExposure(self.textBoxLightTime2))
        #layout.addWidget(buttonLightplus2, 6,3)
        self.textBoxLightTime2 = QLineEdit()
        self.textBoxLightTime2.setStyleSheet("height: 100")
        self.textBoxLightTime2.setFont(self.textFont)
        self.textBoxLightTime2.setReadOnly(True)
        #self.textBoxLightTime2.setText(str(Exposure_Time_Default))
        #layout.addWidget(self.textBoxLightTime2, 6,1,1,2)
        buttonLightminus2 = QPushButton("-")
        buttonLightminus2.setStyleSheet("height: 100")
        buttonLightminus2.setFont(self.textFont)
        buttonLightminus2.clicked.connect(lambda: self.decreaseExposure(self.textBoxLightTime2))
        #layout.addWidget(buttonLightminus2, 6,0)

        #layout.addWidget(QLabel("tbd:"), 2,2)
        #textBoxType = QLineEdit()
        #layout.addWidget(textBoxType, 2,3)

        self.labelCalibStart1 = QLabel("")
        self.labelCalibStart1.setStyleSheet("color: blue")
        #self.labelCalibStart1.hide()
        layout.addWidget(self.labelCalibStart1, 9,0,1,4)

        self.labelCalibStart2 = QLabel("")
        self.labelCalibStart2.setStyleSheet("color: blue")
        #self.labelCalibStart2.hide()
        #layout.addWidget(self.labelCalibStart2, 8,0,1,4)

        buttonCalibration = QPushButton("Kalibrierung")
        buttonCalibration.setFont(self.textFont)
        buttonCalibration.setStyleSheet("height: 100")
        buttonCalibration.pressed.connect(self.calibrateCams)
        layout.addWidget(buttonCalibration, 8,0,1,4)

        labelPlace = QLabel("")
        #labelInterval.setFont(self.textFont2)
        layout.addWidget(labelPlace, 7,0)

        labelPlace2 = QLabel("")
        #labelInterval.setFont(self.textFont2)
        #layout.addWidget(labelPlace2, 9,0)

        #labelExposure = QLabel("Beleuchtung(%):")
        #labelExposure.setFont(self.textFont2)
        #layout.addWidget(labelExposure, 4,0)
        #textBoxExposure = QLineEdit()
        #textBoxExposure.setStyleSheet("height: 100")
        #textBoxExposure.setFont(self.textFont)
        #layout.addWidget(textBoxExposure, 4,1)
        #textBoxExposure.setReadOnly(True)
        #textBoxExposure.setText("58")

        buttonCancel = QPushButton("Zurück OHNE Änderungen")
        buttonCancel.pressed.connect(self.returnNoSaving)
        buttonCancel.setFont(self.ButtonFont)
        buttonCancel.setStyleSheet("background-color: red; height: 100; color: white")
        layout.addWidget(buttonCancel, 10,0,1,2)

        buttonSave = QPushButton("Zurück && Änderungen übernehmen")
        buttonSave.pressed.connect(self.saveCameraSettings)
        buttonSave.setFont(self.ButtonFont)
        buttonSave.setStyleSheet("background-color: green; height: 100; color: white")
        layout.addWidget(buttonSave, 10,2,1,2)

        self.stack2.setLayout(layout)

    def logs(self):
        """
        Log Dateien Seite
        """
        layout = QGridLayout()
        labelHeadline = QLabel("Einstellungen: Logs")
        labelHeadline.setFont(self.textFont)
        layout.addWidget(labelHeadline, 0,0,1,2)

        self.labelEStatus = QLabel("E-Mail(s) werden gesendet")
        self.labelEStatus.setStyleSheet("background-color: blue; color: white")
        self.labelEStatus.setAlignment(Qt.AlignCenter)
        self.labelEStatus.hide()
        layout.addWidget(self.labelEStatus, 0,2,1,2)

        self.tableLogs = QTableWidget()
        self.tableLogs.setStyleSheet('QAbstractItemView::indicator {width: 300px; height: 120px;}');
        self.tableLogs.setColumnCount(3)
        self.tableLogs.setColumnWidth(0,425)
        self.tableLogs.setColumnWidth(1,425)
        self.tableLogs.setColumnWidth(2,300)
        self.tableLogs.setHorizontalHeaderLabels(LOGS)
        layout.addWidget(self.tableLogs, 1,0,1,4)

        setLogData(self.tableLogs, self.logfiles)

        buttonCancel = QPushButton("Zurück")
        buttonCancel.pressed.connect(self.returnNoSaving)
        buttonCancel.setFont(self.ButtonFont)
        buttonCancel.setStyleSheet("background-color: red; height: 100; color: white")
        layout.addWidget(buttonCancel, 3,0,1,2)

        self.buttonSendLogs = QPushButton("Senden per email")
        self.buttonSendLogs.pressed.connect(self.startELogThread)
        self.buttonSendLogs.setFont(self.ButtonFont)
        self.buttonSendLogs.setStyleSheet("background-color: green; height: 100; color: white")
        layout.addWidget(self.buttonSendLogs, 3,2,1,2)

        self.stack3.setLayout(layout)

    def newDataset(self):
        """
        Seite zum Inut der Datensatz Informationen
        """

        layout = QGridLayout()
        labelHeadline = QLabel("Neuen Datensatz anlegen")
        labelHeadline.setFont(self.textFont)
        layout.addWidget(labelHeadline, 0,0,1,2)

        self.buttonStartND = QPushButton("Fotoaufnahme starten")
        self.buttonDatasetND = QPushButton("Datensatz abschließen und hochladen")

        labelCultivation = QLabel("Kultur*:")
        labelCultivation.setFont(self.textFont)
        layout.addWidget(labelCultivation, 1,0)
        self.comboBoxCultivation = QComboBox()
        self.comboBoxCultivation.setStyleSheet("height: 100")
        self.comboBoxCultivation.setFont(self.textFont)
        self.comboBoxCultivation.addItems(CULTIVATION)
        self.comboBoxCultivation.currentTextChanged.connect(lambda: self.checkText(0, self.comboBoxCultivation, self.buttonStartND, self.buttonDatasetND))
        layout.addWidget(self.comboBoxCultivation, 1,1)

        labelBBCH = QLabel("BBCH*:")
        labelBBCH.setFont(self.textFont)
        layout.addWidget(labelBBCH, 1,2)
        self.comboBoxBBCH = QComboBox()
        self.comboBoxBBCH.setStyleSheet("height: 100")
        self.comboBoxBBCH.setFont(self.textFont)
        self.comboBoxBBCH.addItems(BBCH)
        self.comboBoxBBCH.currentTextChanged.connect(lambda: self.checkText(1,  self.comboBoxBBCH, self.buttonStartND, self.buttonDatasetND))
        layout.addWidget(self.comboBoxBBCH, 1,3)

        labelLight = QLabel("Licht*:")
        labelLight.setFont(self.textFont)
        layout.addWidget(labelLight, 2,0)
        self.comboBoxLight = QComboBox()
        self.comboBoxLight.setStyleSheet("height: 100")
        self.comboBoxLight.setFont(self.textFont)
        self.comboBoxLight.addItems(LIGHT)
        self.comboBoxLight.currentTextChanged.connect(lambda: self.checkText(2, self.comboBoxLight, self.buttonStartND, self.buttonDatasetND))
        layout.addWidget(self.comboBoxLight, 2,1)

        labelGround = QLabel("Boden*:")
        labelGround.setFont(self.textFont)
        layout.addWidget(labelGround, 3,0)
        self.comboBoxGround = QComboBox()
        self.comboBoxGround.setStyleSheet("height: 100")
        self.comboBoxGround.setFont(self.textFont)
        self.comboBoxGround.addItems(GROUND)
        self.comboBoxGround.currentTextChanged.connect(lambda: self.checkText(3, self.comboBoxGround, self.buttonStartND, self.buttonDatasetND))
        layout.addWidget(self.comboBoxGround, 3,1)

        self.buttonStartND.clicked.connect(lambda: self.Stack.setCurrentIndex(8))
        self.buttonStartND.clicked.connect(lambda: self.setRecordingStatus(True))
        self.buttonStartND.pressed.connect(self.saveDatasetSettings)
        self.buttonStartND.setFont(self.ButtonFont)
        self.buttonStartND.setEnabled(False)
        self.buttonStartND.setStyleSheet("background-color: grey; height: 100; color: white")
        layout.addWidget(self.buttonStartND, 16,2,1,2)


        self.buttonDatasetND.pressed.connect(self.endDataset)
        self.buttonDatasetND.setFont(self.ButtonFont)
        self.buttonDatasetND.setStyleSheet("background-color: green; height: 100; color: white")
        self.buttonDatasetND.setHidden(True)
        layout.addWidget(self.buttonDatasetND, 16,2,1,2)

        #labelBusiness = QLabel("Betrieb:")
        #labelBusiness.setFont(self.textFont2)
        #layout.addWidget(labelBusiness, 3,0)
        #self.textBoxBusiness = QLineEdit()
        #self.textBoxBusiness.setStyleSheet("height: 100")
        #self.textBoxBusiness.setFont(self.textFont)
        #self.textBoxBusiness.textChanged.connect(lambda: self.checkText(4, self.textBoxBusiness, self.buttonStartND, self.buttonDatasetND))
        #layout.addWidget(self.textBoxBusiness, 3,1)

        self.labelNotice = QLabel("!Hinweis! Datensatz nicht \n vollständig: (Bilder:")
        self.labelNotice.setStyleSheet("background-color: yellow")
        self.labelNotice.setAlignment(Qt.AlignCenter)
        self.labelNotice.hide()
        layout.addWidget(self.labelNotice, 0,2,1,2)

        #self.buttonStartND.clicked.connect(lambda:
        #writeLog("login", ""))

        #labelFieldname = QLabel("Feldname:")
        #labelFieldname.setFont(self.textFont2)
        #layout.addWidget(labelFieldname, 4,0)
        #self.textBoxFieldname = QLineEdit()
        #self.textBoxFieldname.setStyleSheet("height: 100")
        #self.textBoxFieldname.setFont(self.textFont)
        #self.textBoxFieldname.textChanged.connect(lambda: self.checkText(5, self.textBoxFieldname, self.buttonStartND, self.buttonDatasetND))
        #layout.addWidget(self.textBoxFieldname, 4,1)

        labelDistance = QLabel("Wuchshöhe(cm)*:")
        labelDistance.setFont(self.textFont)
        layout.addWidget(labelDistance, 2,2)
        self.comboBoxDistance = QComboBox()
        self.comboBoxDistance.setStyleSheet("height: 100")
        self.comboBoxDistance.setFont(self.textFont)
        self.comboBoxDistance.addItem("")
        n = 1
        while n <= 120:
            self.comboBoxDistance.addItem(str(n))
            if n < 30:
                n = n + 1
            elif n < 50:
                n = n + 2
            else:
                n = n + 5
        self.comboBoxDistance.currentTextChanged.connect(lambda: self.checkText(4, self.comboBoxDistance, self.buttonStartND, self.buttonDatasetND))
        #self.textBoxDistance.setFont(self.textFont)
        #self.textBoxDistance.textChanged.connect(lambda: self.checkText(7, self.textBoxDistance, self.buttonStartND, self.buttonDatasetND))
        layout.addWidget(self.comboBoxDistance, 2,3)

        labelType = QLabel("Sorte*:")
        labelType.setFont(self.textFont)
        layout.addWidget(labelType, 3,2)
        self.textBoxType = QLineEdit()
        self.textBoxType.setStyleSheet("height: 100px")
        self.textBoxType.setFont(self.textFont)
        self.textBoxType.textChanged.connect(lambda: self.checkText(5, self.textBoxType, self.buttonStartND, self.buttonDatasetND))
        layout.addWidget(self.textBoxType, 3,3)

        labelInfluences = QLabel("Umwelteinflüsse:")
        labelInfluences.setFont(self.textFont)
        layout.addWidget(labelInfluences, 6,0,1,4)
        self.comboBoxInfluences = QComboBox()
        self.comboBoxInfluences.setStyleSheet("height: 100")
        self.comboBoxInfluences.setFont(self.textFont)
        self.comboBoxInfluences.addItems(INFLUENCES)
        layout.addWidget(self.comboBoxInfluences, 7,0,1,4)

        labelInfestation = QLabel("Verunkrautung:")
        labelInfestation.setFont(self.textFont)
        layout.addWidget(labelInfestation, 8,0,1,4)
        self.comboBoxInfestation = QComboBox()
        self.comboBoxInfestation.setStyleSheet("height: 100")
        self.comboBoxInfestation.setFont(self.textFont)
        self.comboBoxInfestation.addItems(INFESTATION)
        layout.addWidget(self.comboBoxInfestation, 9,0,1,4)

        #layout.addWidget(QLabel("tbd:"), 5,2)
        #self.textBoxTBD = QLineEdit()
        #self.textBoxTBD.textChanged.connect(lambda: self.checkText(4, self.textBoxTBD, self.buttonStartND))
        #layout.addWidget(self.textBoxTBD, 5,3)

        #labelComment = QLabel("Kommentar:")
        #labelComment.setFont(self.textFont2)
        #layout.addWidget(labelComment, 7,0)
        #self.textBoxComment = QTextEdit()
        #self.textBoxComment.setStyleSheet("height: 200")
        #self.textBoxComment.setFont(self.textFont)
        #layout.addWidget(self.textBoxComment, 7,1,1,3)

        labelPlace = QLabel("")
        layout.addWidget(labelPlace, 15,0)

        #labelPlace2 = QLabel("")
        #layout.addWidget(labelPlace2, 11,0)

        self.buttonCancelND = QPushButton("Abbruch")
        self.buttonCancelND.clicked.connect(lambda:
        self.Stack.setCurrentIndex(0))
        self.buttonCancelND.setFont(self.ButtonFont)
        self.buttonCancelND.setStyleSheet("background-color: red; height: 100; color: white")
        layout.addWidget(self.buttonCancelND, 16,0,1,2)

        self.buttonReturnND = QPushButton("Zurück")
        self.buttonReturnND.pressed.connect(self.returnToCam)
        self.buttonReturnND.setFont(self.ButtonFont)
        self.buttonReturnND.setStyleSheet("background-color: red; height: 100; color: white")
        self.buttonReturnND.setHidden(True)
        layout.addWidget(self.buttonReturnND, 16,0,1,2)

        self.buttonReturnND2 = QPushButton("Zurück OHNE Änderungen")
        self.buttonReturnND2.pressed.connect(self.returnNoSaving)
        self.buttonReturnND2.setFont(self.ButtonFont)
        self.buttonReturnND2.setStyleSheet("background-color: red; height: 100; color: white")
        self.buttonReturnND2.setHidden(True)
        layout.addWidget(self.buttonReturnND2, 16,0,1,2)

        self.buttonSaveND = QPushButton("Zurück && Änderungen übernehmen")
        self.buttonSaveND.pressed.connect(self.returnWithSaving)
        self.buttonSaveND.setFont(self.ButtonFont)
        self.buttonSaveND.setStyleSheet("background-color: green; height: 100; color: white")
        self.buttonSaveND.setHidden(True)
        layout.addWidget(self.buttonSaveND, 16,2,1,2)


        self.stack4.setLayout(layout)

    def recording(self):
        """
        Fotoaufnahme/Live-Stream
        """

        layout = QGridLayout()

        self.labelImage2 = QLabel()
        #self.labelImage2.setHidden(True)
        #self.labelImage2.setStyleSheet("width: 200")
        #layout.addWidget(self.labelImage2, 3,0,1,6)

        self.labelZoom = QLabel()
        #self.labelZoom.setHidden(True)
        layout.addWidget(self.labelZoom, 3,0,1,6)

        self.labelStream2 = QLabel()
        self.labelStream2.setStyleSheet("qproperty-alignment: AlignCenter")
        layout.addWidget(self.labelStream2, 1,0,1,6)

        self.buttonLImage2 = QPushButton("Letztes Bild")
        self.buttonLImage2.setStyleSheet("height: 60")
        self.buttonLImage2.setFont(self.textFont2)
        self.buttonLImage2.pressed.connect(lambda:
        self.switchImageStream(2, self.buttonLImage2))
        #layout.addWidget(self.buttonLImage2, 0,2)

        self.buttonCancel = QPushButton("Abbruch")
        self.buttonCancel.setFont(self.textFont2)
        self.buttonCancel.clicked.connect(lambda:
        self.Stack.setCurrentIndex(7))
        self.buttonCancel.clicked.connect(lambda: self.triggerImage(False))
        self.buttonCancel.setStyleSheet("background-color: red; height: 100; color: white")
        layout.addWidget(self.buttonCancel, 2,0)

        if self.comboBoxTrigger.currentText() == "manuell":
            textTrigger = "Manuel Auslösung"
        else:
            textTrigger = "Auto Auslösung"

        self.labelTriggerText = QLabel(textTrigger)
        self.labelTriggerText.setFont(self.textFont2)

        layout.addWidget(self.labelTriggerText,2,1)

        self.buttonTakePicture = QPushButton("Bild aufnehmen")
        self.buttonTakePicture.setFont(self.textFont2)
        self.buttonTakePicture.setStyleSheet("background-color: orange; height: 100")
        layout.addWidget(self.buttonTakePicture, 2,2)
        self.buttonTakePicture.pressed.connect(self.start_ImagesThread)

        self.buttonBreak = QPushButton("Pause")
        self.buttonBreak.setFont(self.textFont2)
        self.buttonBreak.setStyleSheet("background-color: orange; height: 100")
        self.buttonBreak.setHidden(True)
        layout.addWidget(self.buttonBreak, 2,2)
        self.buttonBreak.pressed.connect(self.pauseMakingImages)

        self.buttonResume = QPushButton("Fortfahren")
        self.buttonResume.setFont(self.textFont2)
        self.buttonResume.setStyleSheet("background-color: orange; height: 100")
        self.buttonResume.setHidden(True)
        layout.addWidget(self.buttonResume, 2,2)
        self.buttonResume.pressed.connect(self.resumeMakingImages)

        self.labelCountdown = QLabel()
        self.labelCountdown.setHidden(True)
        layout.addWidget(self.labelCountdown,2,3)

        self.labelPicturesNum = QLabel("Bilder: 0 / " + str(self.maxImages))
        self.labelPicturesNum.setFont(self.textFont2)
        layout.addWidget(self.labelPicturesNum,2,4)

        self.buttonComplete = QPushButton("Aufnahme abschließen")
        self.buttonComplete.setFont(self.textFont2)
        self.buttonComplete.pressed.connect(self.endRecording)
        self.buttonComplete.setStyleSheet("background-color: green; height: 100; color: white")
        layout.addWidget(self.buttonComplete, 2,5)

        self.labelStream = QLabel()
        layout.addWidget(self.labelStream,1,0,1,6)

        self.labelImage = QLabel()
        self.labelImage.setStyleSheet("qproperty-alignment: AlignCenter")
        #self.labelImage.setHidden(True)
        layout.addWidget(self.labelImage, 3,0,1,6)

        self.buttonZoomIn = QPushButton("+")
        self.buttonZoomIn.setFont(self.textFontZoom)
        self.buttonZoomIn.pressed.connect(lambda:
        self.zoomImage("plus", False))
        self.buttonZoomIn.setStyleSheet("height: 80")
        layout.addWidget(self.buttonZoomIn, 4,0,1,2)

        self.buttonOriginal = QPushButton("original")
        self.buttonOriginal.setFont(self.textFont2)
        self.buttonOriginal.pressed.connect(lambda:
        self.zoomImage("original", False))
        self.buttonOriginal.setStyleSheet("height: 80")
        layout.addWidget(self.buttonOriginal, 4,2,1,3)

        self.buttonZoomOut = QPushButton("-")
        self.buttonZoomOut.setFont(self.textFontZoom)
        self.buttonZoomOut.pressed.connect(lambda:
        self.zoomImage("minus", False))
        #self.buttonZoomOut.setGeometry(0,0, 80, 80)
        self.buttonZoomOut.setStyleSheet("height: 80")
        layout.addWidget(self.buttonZoomOut, 4,5,1,1)

        self.buttonLImage = QPushButton("Letztes Bild")
        self.buttonLImage.setFont(self.textFont)
        self.buttonLImage.setStyleSheet("height: 60")
        self.buttonLImage.pressed.connect(lambda:
        self.switchImageStream(1, self.buttonLImage))
        #layout.addWidget(self.buttonLImage, 4,2)

        self.stack5.setLayout(layout)

    def adminCheck(self):
        """
        Sicherheitslayer Pin Code eingabe
        """

        layout = QGridLayout()
        labelHeadline = QLabel("Einstellungen: Admin")
        labelHeadline.setFont(self.textFont)
        layout.addWidget(labelHeadline, 0,0,1,2)

        #layout.addWidget(QLabel("admin PIN"), 1,0)
        self.textBoxPIN = QLineEdit()
        self.textBoxPIN.setStyleSheet("height: 100")
        self.textBoxPIN.setFont(self.textFont)
        self.textBoxPIN.setReadOnly(True)
        layout.addWidget(self.textBoxPIN, 1,0,1,3)

        button1 = QPushButton("1")
        button1.setFont(self.textFont2)
        button1.setStyleSheet("height: 100")
        layout.addWidget(button1, 2,0)
        button1.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "1"))

        button2 = QPushButton("2")
        button2.setFont(self.textFont2)
        button2.setStyleSheet("height: 100")
        layout.addWidget(button2, 2,1)
        button2.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "2"))

        button3 = QPushButton("3")
        button3.setFont(self.textFont2)
        button3.setStyleSheet("height: 100")
        layout.addWidget(button3, 2,2)
        button3.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "3"))

        button4 = QPushButton("4")
        button4.setFont(self.textFont2)
        button4.setStyleSheet("height: 100")
        layout.addWidget(button4, 3,0)
        button4.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "4"))

        button5 = QPushButton("5")
        button5.setFont(self.textFont2)
        button5.setStyleSheet("height: 100")
        layout.addWidget(button5, 3,1)
        button5.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "5"))

        button6 = QPushButton("6")
        button6.setFont(self.textFont2)
        button6.setStyleSheet("height: 100")
        layout.addWidget(button6, 3,2)
        button6.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "6"))

        button7 = QPushButton("7")
        button7.setFont(self.textFont2)
        button7.setStyleSheet("height: 100")
        layout.addWidget(button7, 4,0)
        button7.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "7"))

        button8 = QPushButton("8")
        button8.setFont(self.textFont2)
        button8.setStyleSheet("height: 100")
        layout.addWidget(button8, 4,1)
        button8.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "8"))

        button9 = QPushButton("9")
        button9.setFont(self.textFont2)
        button9.setStyleSheet("height: 100")
        layout.addWidget(button9, 4,2)
        button9.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "9"))

        buttonDelete = QPushButton("<-")
        buttonDelete.setFont(self.textFont2)
        buttonDelete.setStyleSheet("background-color: red; height: 100")
        layout.addWidget(buttonDelete, 5,0)
        buttonDelete.clicked.connect(lambda:
        deletePinNumber(self.textBoxPIN))

        button0 = QPushButton("0")
        button0.setFont(self.textFont2)
        button0.setStyleSheet("height: 100")
        layout.addWidget(button0, 5,1)
        button0.clicked.connect(lambda:
        setPinNumber(self.textBoxPIN, "0"))

        buttonOK = QPushButton("OK")
        buttonOK.setFont(self.textFont2)
        buttonOK.pressed.connect(self.checkPin)
        buttonOK.clicked.connect(lambda:
        deleteText(self.textBoxPIN))
        buttonOK.setStyleSheet("background-color: green; height: 100")
        layout.addWidget(buttonOK, 5,2)

        buttonCancel = QPushButton("Zurück")
        buttonCancel.setFont(self.textFont2)
        buttonCancel.clicked.connect(lambda:
        self.Stack.setCurrentIndex(0))
        buttonCancel.clicked.connect(lambda:
        deleteText(self.textBoxPIN))
        buttonCancel.setStyleSheet("background-color: red; height: 100")
        layout.addWidget(buttonCancel, 6,0)

        self.buttonCamera.clicked.connect(lambda:
        deleteText(self.textBoxPIN))

        self.buttonLogs.clicked.connect(lambda:
        deleteText(self.textBoxPIN))

        self.buttonAdmin.clicked.connect(lambda:
        deleteText(self.textBoxPIN))

        self.stack6.setLayout(layout)

    def adminSettings(self):
        """
        Admin Einstellungen
        """

        layout = QGridLayout()
        labelHeadline = QLabel("Einstellungen: Admin")
        labelHeadline.setFont(self.textFont)
        layout.addWidget(labelHeadline, 0,0,1,2)

        labelDevice = QLabel("Gerät:")
        labelDevice.setFont(self.textFont2)
        layout.addWidget(labelDevice, 1,0)
        self.comboBoxDevice = QComboBox()
        self.comboBoxDevice.setStyleSheet("height: 100")
        self.comboBoxDevice.setFont(self.textFont)
        self.comboBoxDevice.addItems(DEVICE)
        layout.addWidget(self.comboBoxDevice, 1,1)

        labelSensor = QLabel("Sensorbox:")
        labelSensor.setFont(self.textFont2)
        layout.addWidget(labelSensor, 2,0)
        self.comboBoxSensor = QComboBox()
        self.comboBoxSensor.setStyleSheet("height: 100")
        self.comboBoxSensor.setFont(self.textFont)
        self.comboBoxSensor.addItems(SENSORBOX)
        layout.addWidget(self.comboBoxSensor, 2,1)

        labelLanguage = QLabel("Sprache:")
        labelLanguage.setFont(self.textFont2)
        layout.addWidget(labelLanguage, 1,2)
        self.comboBoxLanguage = QComboBox()
        self.comboBoxLanguage.setStyleSheet("height: 100")
        self.comboBoxLanguage.setFont(self.textFont)
        self.comboBoxLanguage.addItems(LANGUAGE)
        layout.addWidget(self.comboBoxLanguage, 1,3)

        labelUpload = QLabel("Upload:")
        labelUpload.setFont(self.textFont2)
        #layout.addWidget(labelUpload, 3,0)
        self.comboBoxUpload = QComboBox()
        self.comboBoxUpload.setStyleSheet("height: 100")
        self.comboBoxUpload.setFont(self.textFont)
        self.comboBoxUpload.addItems(UPLOAD)
        #layout.addWidget(self.comboBoxUpload, 3,1)

        #layout.addWidget(QLabel("Zieladresse:"), 2,2)
        #textBoxAdress = QLineEdit()
        #layout.addWidget(textBoxAdress, 2,3)

        labelCameraName1 = QLabel("Kameraname 1:")
        labelCameraName1.setFont(self.textFont2)
        layout.addWidget(labelCameraName1, 5,0)
        self.textBoxCamera1 = QLineEdit("Daheng 6MP")
        self.textBoxCamera1.setStyleSheet("height: 100")
        self.textBoxCamera1.setFont(self.textFont)
        self.textBoxCamera1.setReadOnly(True)
        layout.addWidget(self.textBoxCamera1, 5,1)

        labelMaxImages = QLabel("max. Bilder:")
        labelMaxImages.setFont(self.textFont2)
        layout.addWidget(labelMaxImages, 2,2)
        self.textBoxMaxImages = QLineEdit()
        self.textBoxMaxImages.setStyleSheet("height: 100")
        self.textBoxMaxImages.setFont(self.textFont)
        self.textBoxMaxImages.setText(str(self.maxImages))
        layout.addWidget(self.textBoxMaxImages, 2,3)

        labelCamera1 = QLabel("Kamera 1:")
        labelCamera1.setFont(self.textFont2)
        layout.addWidget(labelCamera1, 4,0)
        self.comboBoxCamera1 = QComboBox()
        self.comboBoxCamera1.setStyleSheet("height: 100")
        self.comboBoxCamera1.setFont(self.textFont)
        self.comboBoxCamera1.addItems(CAMERA)
        layout.addWidget(self.comboBoxCamera1, 4,1)

        labelNewPin = QLabel("Neue Pin angeben:")
        labelNewPin.setFont(self.textFont2)
        layout.addWidget(labelNewPin, 3,2)
        self.textBoxNewPin = QLineEdit()
        self.textBoxNewPin.setStyleSheet("height: 100")
        self.textBoxNewPin.setFont(self.textFont)
        onlyInt = QIntValidator()
        #onlyInt.setRange(0, 4)
        self.textBoxNewPin.setValidator(onlyInt)
        layout.addWidget(self.textBoxNewPin, 3,3)

        labelCamera2 = QLabel("Kamera 2:")
        labelCamera2.setFont(self.textFont2)
        layout.addWidget(labelCamera2, 4,2)
        self.comboBoxCamera2 = QComboBox()
        self.comboBoxCamera2.setStyleSheet("height: 100")
        self.comboBoxCamera2.setFont(self.textFont)
        self.comboBoxCamera2.addItems(CAMERA)
        layout.addWidget(self.comboBoxCamera2, 4,3)

        labelCameraName2 = QLabel("Kameraname 2:")
        labelCameraName2.setFont(self.textFont2)
        layout.addWidget(labelCameraName2, 5,2)
        self.textBoxCamera2 = QLineEdit("ArduCam")
        self.textBoxCamera2.setStyleSheet("height: 100")
        self.textBoxCamera2.setFont(self.textFont)
        self.textBoxCamera2.setReadOnly(True)
        layout.addWidget(self.textBoxCamera2, 5,3)

        labelServer = QLabel("Server:")
        labelServer.setFont(self.textFont2)
        layout.addWidget(labelServer, 3,0)
        self.comboBoxServer = QComboBox()
        self.comboBoxServer.setStyleSheet("height: 100")
        self.comboBoxServer.setFont(self.textFont)
        self.comboBoxServer.addItems(SERVER)
        layout.addWidget(self.comboBoxServer, 3,1)

        """
        labelFPSMax = QLabel("FPS-max:")
        labelFPSMax.setFont(self.textFont2)
        layout.addWidget(labelFPSMax, 6,2)
        textBoxFPSMax = QLineEdit()
        textBoxFPSMax.setStyleSheet("height: 100")
        textBoxFPSMax.setFont(self.textFont)
        textBoxFPSMax.setReadOnly(True)
        layout.addWidget(textBoxFPSMax, 6,3)

        labelFPSMin = QLabel("FPS-min:")
        labelFPSMin.setFont(self.textFont2)
        layout.addWidget(labelFPSMin, 7,2)
        textBoxFPSMin = QLineEdit()
        textBoxFPSMin.setStyleSheet("height: 100")
        textBoxFPSMin.setFont(self.textFont)
        textBoxFPSMin.setReadOnly(True)
        layout.addWidget(textBoxFPSMin, 7,3)
        """
        layout.addWidget(QLabel(""), 8,0)
        layout.addWidget(QLabel(""), 9,0)
        layout.addWidget(QLabel(""), 10,0)

        buttonCancel = QPushButton("Zurück OHNE Änderungen")
        buttonCancel.pressed.connect(self.returnNoSaving)
        buttonCancel.setFont(self.ButtonFont)
        buttonCancel.setStyleSheet("background-color: red; height: 100; color: white")
        layout.addWidget(buttonCancel, 11,0,1,2)

        buttonSave = QPushButton("Zurück && Änderungen übernehmen")
        #buttonSave.clicked.connect(lambda:
        #self.Stack.setCurrentIndex(5))
        buttonSave.pressed.connect(self.saveAdminSettings)
        buttonSave.setFont(self.ButtonFont)
        buttonSave.setStyleSheet("background-color: green; height: 100; color: white")
        layout.addWidget(buttonSave, 11,2,1,2)

        self.stack7.setLayout(layout)

    def query(self):
        """
        Sicherheitsabfrage
        """

        layout = QGridLayout()

        labelQuery = QLabel("Wollen Sie wirklich alle Bilder dieses \n Datensatzes löschen?")
        labelQuery.setFont(QFont('Times', 20))
        layout.addWidget(labelQuery, 0,0,1,3)

        buttonContinue = QPushButton("Ja")
        buttonContinue.pressed.connect(self.cancelRecording)
        buttonContinue.setFont(self.ButtonFont)
        buttonContinue.setStyleSheet("background-color: red; height: 100; color: white")
        layout.addWidget(buttonContinue,1,0)

        buttonCancel = QPushButton("Zurück")
        buttonCancel.clicked.connect(lambda:
        self.Stack.setCurrentIndex(4))
        buttonCancel.clicked.connect(lambda: self.triggerImage(True))
        buttonCancel.setFont(self.ButtonFont)
        buttonCancel.setStyleSheet("background-color: green; height: 100; color: white")
        layout.addWidget(buttonCancel, 1,1)

        self.stack8.setLayout(layout)

    def cameraCalib(self):
        """
        Seite zum Klaibrieren der Kameras
        """

        layout = QGridLayout()

        labelCalib = QLabel("Kalibrierung der Kamera(s):")
        labelCalib.setFont(self.textFont)
        layout.addWidget(labelCalib, 0,0,1,2)

        self.labelStreamCalib = QLabel()
        layout.addWidget(self.labelStreamCalib,1,0,1,2)

        buttonCalibration = QPushButton("Kalibrierung")
        buttonCalibration.setFont(self.textFont2)
        buttonCalibration.setStyleSheet("height: 100")
        buttonCalibration.pressed.connect(self.calibrateCams)
        layout.addWidget(buttonCalibration, 2,0,1,2)

        self.labelCalibCam1 = QLabel("")
        self.labelCalibCam1.setStyleSheet("color: blue")
        layout.addWidget(self.labelCalibCam1, 3,0,1,2)

        self.labelCalibCam2 = QLabel("")
        self.labelCalibCam2.setStyleSheet("color: blue")
        layout.addWidget(self.labelCalibCam2, 4,0,1,2)

        buttonCancel = QPushButton("Zurück")
        buttonCancel.setFont(self.textFont2)
        buttonCancel.setStyleSheet("background-color: red; height: 100; color: white")
        #buttonCancel.clicked.connect(lambda:
        #self.Stack.setCurrentIndex(3))
        buttonCancel.pressed.connect(self.cancelCalib)
        layout.addWidget(buttonCancel, 5,0)

        buttonContinue = QPushButton("Fortfahren")
        buttonContinue.setFont(self.textFont2)
        buttonContinue.setStyleSheet("background-color: green; height: 100; color: white")
        #buttonContinue.clicked.connect(lambda:
        #self.Stack.setCurrentIndex(4))
        buttonContinue.clicked.connect(lambda: self.triggerImage(True))
        buttonContinue.pressed.connect(self.addNewDataset)
        buttonContinue.clicked.connect(lambda: self.endCalib())
        layout.addWidget(buttonContinue,5,1)

        self.stack9.setLayout(layout)

    def queryDelete(self):
        """
        Sicherheitsabfrage
        """

        layout = QGridLayout()

        labelQuery = QLabel("Wollen Sie wirklich die ausgewählten \n Datensätze löschen?")
        labelQuery.setFont(QFont('Times', 20))
        layout.addWidget(labelQuery, 0,0,1,3)

        buttonContinue = QPushButton("Ja")
        buttonContinue.pressed.connect(self.deleteSelectedDataset)
        buttonContinue.setFont(self.ButtonFont)
        buttonContinue.setStyleSheet("background-color: red; height: 100; color: white")
        layout.addWidget(buttonContinue,1,0)

        buttonCancel = QPushButton("Zurück")
        buttonCancel.clicked.connect(lambda:
        self.Stack.setCurrentIndex(0))
        buttonCancel.setFont(self.ButtonFont)
        buttonCancel.setStyleSheet("background-color: green; height: 100; color: white")
        layout.addWidget(buttonCancel, 1,1)

        self.stack10.setLayout(layout)

    def fokusPage(self):
        """
        Bild fokusierung
        """
        layout = QGridLayout()

        self.buttonDStream = QPushButton("Fokussierung starten")
        self.buttonDStream.setFont(self.textFont2)
        self.buttonDStream.pressed.connect(self.startDahengStream)
        self.buttonDStream.setStyleSheet("height: 100")
        layout.addWidget(self.buttonDStream, 0,0,1,3)

        buttonEndFokus = QPushButton("Fokussierung beenden")
        buttonEndFokus.setFont(self.textFont2)
        buttonEndFokus.clicked.connect(lambda:
        self.Stack.setCurrentIndex(0))
        buttonEndFokus.setStyleSheet("height: 100")
        layout.addWidget(buttonEndFokus, 0,3,1,3)

        self.labelDahengStream = QLabel()
        self.labelDahengStream.setStyleSheet("qproperty-alignment: AlignRight")
        layout.addWidget(self.labelDahengStream, 1,0,4,6)

        self.buttonZoomIn2 = QPushButton("+")
        self.buttonZoomIn2.setFont(self.textFontZoom)
        self.buttonZoomIn2.pressed.connect(lambda:
        self.zoomImage("plus", True))
        self.buttonZoomIn2.setStyleSheet("height: 80")
        layout.addWidget(self.buttonZoomIn2, 5,0,1,2)

        self.buttonOriginal2 = QPushButton("original")
        self.buttonOriginal2.setFont(self.textFont2)
        self.buttonOriginal2.pressed.connect(lambda:
        self.zoomImage("original", True))
        self.buttonOriginal2.setStyleSheet("height: 80")
        layout.addWidget(self.buttonOriginal2, 5,2,1,2)

        self.buttonZoomOut2 = QPushButton("-")
        self.buttonZoomOut2.setFont(self.textFontZoom)
        self.buttonZoomOut2.pressed.connect(lambda:
        self.zoomImage("minus", True))
        self.buttonZoomOut2.setStyleSheet("height: 80")
        layout.addWidget(self.buttonZoomOut2, 5,4,1,2)

        layout.addWidget(QLabel(""), 6,0)


        self.stack11.setLayout(layout)


    def display(self,i):
        self.Stack.setCurrentIndex(i)

    def show_new_window(self):
            try:
                self.infoWindow = InfoWindow()
                self.infoWindow.show()
            except Exception as e:
                eMessage = "Displaying Info Window failed \n" + str(e)
                print(eMessage)
                writeLog("Error", eMessage)

    def pageChanged(self):
        try:
            self.lastPage =  self.currentPage
            self.currentPage = self.Stack.currentIndex()

            #self.labelBattery.setText(str(self.lastPage))

            if self.currentPage == 0:
                self.buttonDataset.setHidden(True)
            else:
                self.buttonDataset.setHidden(False)

            if self.currentPage == 1 or self.currentPage == 3 or self.currentPage == 6 or self.currentPage == 8:
                self.buttonCamera.setEnabled(False)
                self.buttonLogs.setEnabled(False)
                self.buttonDataset.setEnabled(False)
            else:
                self.buttonCamera.setEnabled(True)
                self.buttonLogs.setEnabled(True)
                self.buttonDataset.setEnabled(True)

            if self.currentPage == 1 or self.currentPage == 3 or self.currentPage == 6 or self.currentPage == 4 or self.currentPage == 8:
                self.buttonAdmin.setEnabled(False)
                self.buttonFokus.setEnabled(False)
            else:
                self.buttonAdmin.setEnabled(True)
                self.buttonFokus.setEnabled(True)

            if self.currentPage == 1:
                self.buttonCamera.setStyleSheet("height: 70; background-color: grey")
            else:
                self.buttonCamera.setStyleSheet("height: 70")

            if self.currentPage == 2:
                self.buttonLogs.setStyleSheet("height: 70; background-color: grey")
            else:
                self.buttonLogs.setStyleSheet("height: 70")

            if self.currentPage == 3:
                self.buttonDataset.setStyleSheet("height: 70; background-color: grey")
            else:
                self.buttonDataset.setStyleSheet("height: 70")

            if self.currentPage == 5 or self.currentPage == 6:
                self.buttonAdmin.setStyleSheet("height: 70; background-color: grey")
            else:
                self.buttonAdmin.setStyleSheet("height: 70")

            if self.currentPage == 10:
                self.buttonFokus.setStyleSheet("height: 70; background-color: grey")
            else:
                self.buttonFokus.setStyleSheet("height: 70")
        except Exception as e:
            eMessage = "Changing Sides failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def triggerImage(self, status):
        """
        Setzt die Möglichkeit Bilder über denn manuellen
        Trigger zu starten auf Ture oder False
        """
        self.imgMaking = status

    def startDahengStream(self):
        try:
            self.streamImages()
        except Exception as e:
            eMessage = "Starting/Stopping Daheng Stream failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)


    def pauseMakingImages(self):
        """
        Pausieren der Automatischen Bildaufnahme
        """
        try:
            self.buttonBreak.setHidden(True)
            self.buttonResume.setHidden(False)
            self.buttonComplete.setEnabled(True)
            self.buttonCancel.setEnabled(True)
            #self.buttonComplete.setStyleSheet("background-color: green; height: 100; color: white")
            self.buttonCamera.setEnabled(True)
        except Exception as e:
            eMessage = "Pause Image making failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def resumeMakingImages(self):
        """
        Fortsetzen der Automatischen Bildaufnahme
        """
        try:
            self.buttonBreak.setHidden(False)
            self.buttonResume.setHidden(True)
            self.buttonComplete.setEnabled(False)
            self.buttonCancel.setEnabled(False)
            #self.buttonComplete.setStyleSheet("background-color: green; height: 100; color: grey")
            self.buttonCamera.setEnabled(False)
        except Exception as e:
            eMessage = "Resume Image making failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def start_camera(self):
        """
        Starten der Kamera(s) (Daheng)
        """  
        #t2 = Timer(0.5,self.streamImages, args=())
        #t2.start()
        t3 = Timer(0.5,self.showPiCamStream, args=())
        t3.start()


    def streamImages(self):
        """
        Live-Stream Bilder werden ausgegeben (ardumcam)
        """

        try:
            setCameraData("control", "image_name", "preview.jpg")
            setCameraData("control", "soft_capture", "1")
            time.sleep(1)
            n = 0
            noSuccess = True
            while n <= 4 and noSuccess:
                try:
                    filename = Path_Daheng_Preview
                    image = cv2.imread(filename)
                    self.fokusImage = image
                    image = cv2.resize(image, (1200,1077))
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = qimage2ndarray.array2qimage(image)
                    self.labelDahengStream.setPixmap(QPixmap.fromImage(image))
                    noSuccess = False
                except Exception as e:
                    eMessage = "Could not read Image (daheng Live-Stream) \n" + str(e)
                    print(eMessage)
                    writeLog("Error", eMessage)
                    time.sleep(1)
                n = n + 1

        except Exception as e:
            eMessage = "Error: open preview jpeg failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
            #self.labelCam1.setStyleSheet("background-color: red; color: white")

    def showPiCamStream(self):
        """
        Live-Stream der Pi Cam wird ausgegeben
        """
        camIsOn = True
        while self.GuiOn:
            connected = True
            try:
                cap = cv2.VideoCapture('http://192.168.100.2:8000/stream.mjpg')
            except Exception as e:
                eMessage = "Connecting to Pi Cam failed \n" + str(e)
                print(eMessage)
                writeLog("Error", eMessage)
                connected = False
                if camIsOn:
                    self.labelCam2.setStyleSheet("background-color: red; color: white")
                camIsOn = False
                time.sleep(5)

            while connected and self.GuiOn:
                    try:
                        ret, frame = cap.read()
                        if frame is not None:
                            #image = imutils.rotate(frame, 180)
                            image = cv2.resize(frame, (1100,500))
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            image = qimage2ndarray.array2qimage(image)
                            self.labelStream2.setPixmap(QPixmap.fromImage(image))
                            if camIsOn != True:
                                self.labelCam2.setStyleSheet("background-color: green; color: white")
                            camIsOn = True
                            #time.sleep(1)
                        else:
                            connected = False
                            if camIsOn:
                                self.labelCam2.setStyleSheet("background-color: red; color: white")
                            camIsOn = False
                            time.sleep(5)
                    except Exception as e:
                        eMessage = "Getting Pi Cam Image failed \n" + str(e)
                        print(eMessage)
                        writeLog("Error", eMessage)
                        if camIsOn:
                            self.labelCam2.setStyleSheet("background-color: red; color: white")
                        camIsOn = False
                        connected = False
                        time.sleep(5)

    def calibrateCams(self):
        """
        Kameras werden kalibriert
        """
        try:
            setCameraData("control", "do_calibration", "1")
            tCalib = Timer(0.5, self.calibrate, args=())
            tCalib.start()
        except Exception as e:
            eMessage = "Camera calibration failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)


    def calibrate(self):
        """
        Kalibrierung der Kamera (Daheng)
        """

        self.labelCalibStart1.setText("Niedrigauflösende Kamera: Kalibrierung wird durchgeführt")
        self.labelCalibCam1.setText("Niedrigauflösende Kamera: Kalibrierung wird durchgeführt")
        #self.labelCalibStart2.setText("Hochauflösende Kamera: Kalibrierung wird durchgeführt")
        #self.labelCalibCam2.setText("Hochauflösende Kamera: Kalibrierung wird durchgeführt")
        """
        try:
            calibGainCam1 = "Once"
            calibWhiteCam1 = "Once"
            n = 0
            for i, cam in enumerate(self.cams):
                cam.BalanceWhiteAuto.set(gx.GxAutoEntry.ONCE)
                cam.GainAuto.set(gx.GxAutoEntry.ONCE)
                #self.labelBattery.setText(getCameraData("control", "do_calibration"))
            while calibGainCam1 != "Off" and calibWhiteCam1 != "Off":
                calibGainValue1 = (str(cam.GainAuto.get())).split("'")
                calibGainCam1 = calibGainValue1[1]
                calibWhiteValue1 = (str(cam.BalanceWhiteAuto.get())).split("'")
                calibWhiteCam1 = calibGainValue1[1]
            self.labelCalibStart1.setText("Niedrigauflösende Kamera: Kalibrierung abgeschlossen")
            self.labelCalibCam1.setText("Niedrigauflösende Kamera: Kalibrierung abgeschlossen")
        except:
            print("Kalibrating Failed (Niedrigauflösende Kamera)")
            self.labelCalibStart1.setText("Niedrigauflösende Kamera: Kalibrierung fehlgeschlagen")
            self.labelCalibCam1.setText("Niedrigauflösende Kamera: Kalibrierung fehlgeschlagen")
            """
        calibCam2 = "1"
        while calibCam2 != "0":
            calibCam2 = getCameraData("control", "do_calibration")
        self.labelCalibStart1.setText("Niedrigauflösende Kamera: Kalibrierung abgeschlossen")
        self.labelCalibCam1.setText("Niedrigauflösende Kamera: Kalibrierung abgeschlossen")


    def setAdminSettings(self):
        try:
            self.comboBoxLanguage.setCurrentText(self.settingAdmin[0])
            self.comboBoxDevice.setCurrentText(self.settingAdmin[1])
            self.comboBoxSensor.setCurrentText(self.settingAdmin[2])
            self.comboBoxUpload.setCurrentText(self.settingAdmin[3])
            self.comboBoxCamera1.setCurrentText(self.settingAdmin[4])
            self.comboBoxCamera2.setCurrentText(self.settingAdmin[5])
            self.textBoxMaxImages.setText(self.settingAdmin[6])
            self.comboBoxServer.setCurrentText(self.settingAdmin[7])

        except Exception as e: 
            eMessage = "Setting Admin Settings failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def setDatasetValues(self):
        try:
            self.comboBoxCultivation.setCurrentText(self.settingsDataset[0])
            self.comboBoxLight.setCurrentText(self.settingsDataset[1])
            self.comboBoxBBCH.setCurrentText(self.settingsDataset[2])
            self.comboBoxGround.setCurrentText(self.settingsDataset[3])
            self.textBoxType.setText(self.settingsDataset[5])
            self.comboBoxDistance.setCurrentText(self.settingsDataset[4])
            self.comboBoxInfluences.setCurrentText(self.settingsDataset[6])
            self.comboBoxInfestation.setCurrentText(self.settingsDataset[7])

        except Exception as e:
            eMessage = "Setting Dataset Values failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def setCameraSettings(self):
        try:
            self.comboBoxTrigger.setCurrentText(self.settingsCamera[0])
            self.comboBoxInterval.setCurrentText(self.settingsCamera[1])
            self.textBoxLightTime1.setText(self.settingsCamera[2])
            #self.textBoxLightTime2.setText(self.settingsCamera[3])

        except Exception as e:
            eMessage = "Setting Camera Settings failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)



    def saveCameraSettings(self):
        """
        Speichern der Kamera Einstellungen
        """

        try:

            if self.textBoxLightTime1.text() != "":
                #exposureTimeC1 =  float(self.textBoxLightTime1.text())
                #set_exposuretime(exposureTimeC1, self.cams[0])
                setCameraData("daheng_camera", "exposure", self.textBoxLightTime1.text())

            if self.textBoxLightTime2.text() != "":
                setCameraData("arducam_camera", "exposure", self.textBoxLightTime2.text())

            setCameraData("daheng_camera", "make_change", "1")

            self.settingsCamera[0] = self.comboBoxTrigger.currentText()
            self.settingsCamera[1] = self.comboBoxInterval.currentText()
            self.settingsCamera[2] = self.textBoxLightTime1.text()
            self.settingsCamera[3] = self.textBoxLightTime2.text()
            self.labelCalibStart1.setText("")
            self.labelCalibCam1.setText("")

            writeCamSettings(self.settingsCamera)

            changeRecoveryDataset("setting", self.settingsCamera)
        except Exception as e:
            eMessage = "Saving Camera Settings failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        #self.labelBattery.setText(str(self.lastPage))

        if self.recordingStart == True:
            self.Stack.setCurrentIndex(4)
        else:
            self.Stack.setCurrentIndex(0)

    def returnNoSaving(self):
        """
        Es wird zur letzten Seite gewechselt ohne zu Speichern
        """
        self.enteredASettings = False
        try:
            self.buttonDStream.setText("Fokussierung starten")
            if self.currentPage == 3:
                self.buttonReturnND2.setHidden(True)
                self.buttonSaveND.setHidden(True)
                self.buttonCancelND.setHidden(False)
                self.buttonStartND.setHidden(False)

            self.setDatasetValues()
            self.setCameraSettings()
            self.setAdminSettings()

            self.textBoxNewPin.setText("")
            self.labelCalibStart1.setText("")
            self.labelCalibCam1.setText("")
        except Exception as e:
            eMessage = "Going back without saving failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        if self.recordingStart == True:
            self.Stack.setCurrentIndex(4)
        else:
            self.Stack.setCurrentIndex(0)

    def setRecordingStatus(self, status):
        self.recordingStart = status

    def saveDatasetSettings(self):
        """
        Datensatz Informationen werden gespeichert
        """
        try:
            self.settingsDataset[0] = self.comboBoxCultivation.currentText()
            self.settingsDataset[1] = self.comboBoxLight.currentText()
            self.settingsDataset[2] = self.comboBoxBBCH.currentText()
            self.settingsDataset[3] = self.comboBoxGround.currentText()
            self.settingsDataset[4] = self.comboBoxDistance.currentText()
            self.settingsDataset[5] = self.textBoxType.text()
            self.settingsDataset[6] = self.comboBoxInfluences.currentText()
            self.settingsDataset[7] = self.comboBoxInfestation.currentText()

            changeRecoveryDataset("dataset", self.settingsDataset)

            if self.recordingStart:
                updateTable(self.tableDatasets, 1, self.comboBoxCultivation.currentText(), self.datasets)
                updateTable(self.tableDatasets, 2, self.comboBoxBBCH.currentText(), self.datasets)
                updateTable(self.tableDatasets, 3, self.comboBoxLight.currentText(), self.datasets)
                updateTable(self.tableDatasets, 4, self.comboBoxGround.currentText(), self.datasets)
                self.writeDataset()
        except Exception as e:
            eMessage = "Saving Dataset Settings failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)


    def returnWithSaving(self):
        """
        Es wird zur letzten Seite gewechselt und die Daten werden übernommen
        """
        try:
            if self.currentPage == 3:
                self.buttonReturnND2.setHidden(True)
                self.buttonSaveND.setHidden(True)
                self.buttonCancelND.setHidden(False)
                self.buttonStartND.setHidden(False)

            self.saveDatasetSettings()
        except Exception as e:
            eMessage = "Going back and saving failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        if self.recordingStart == True:
            self.Stack.setCurrentIndex(4)
        else:
            self.Stack.setCurrentIndex(0)


    def saveAdminSettings(self):
        """
        Admin Einstellugen werden gespeichert
        """
        self.enteredASettings = False
        try:
            self.buttonDStream.setText("Fokussierung starten")
            imageMax = self.textBoxMaxImages.text()
            if imageMax != "":
                imageText = self.labelPicturesNum.text().split(" ")
                self.labelPicturesNum.setText("Bilder: " + imageText[1] + " / " + imageMax)

            if self.comboBoxCamera1.currentText() == "ON":
                self.cameraStatus[0] = True
                self.labelCam1.setStyleSheet("background-color: green; color: white")
            else:
                self.cameraStatus[0] = False
                self.labelCam1.setStyleSheet("background-color: grey; color: white")

            if self.comboBoxCamera2.currentText() == "ON":
                self.cameraStatus[1] = True
                self.labelCam2.setStyleSheet("background-color: green; color: white")
            else:
                self.cameraStatus[1] = False
                self.labelCam2.setStyleSheet("background-color: grey; color: white")

            if self.textBoxNewPin.text() != "":
                self.pinKey = encryptPin(self.textBoxNewPin.text(), self.pinSalt)
                writeNewKey(self.pinKey, self.pinSalt)
                self.textBoxNewPin.setText("")

            setCameraData("daheng_camera", "make_change", "1")

            self.settingAdmin[0] = self.comboBoxLanguage.currentText()
            self.settingAdmin[1] = self.comboBoxDevice.currentText()
            self.settingAdmin[2] = self.comboBoxSensor.currentText()
            self.settingAdmin[3] = self.comboBoxUpload.currentText()
            self.settingAdmin[4] = self.comboBoxCamera1.currentText()
            self.settingAdmin[5] = self.comboBoxCamera2.currentText()
            self.settingAdmin[6] = self.textBoxMaxImages.text()
            self.settingAdmin[7] = self.comboBoxServer.currentText()

            writeAdminSetting(self.settingAdmin)

        except Exception as e:
            eMessage = "Saving Admin Settings failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.Stack.setCurrentIndex(0)

    def endCalib(self):

        try:
            #print(self.imagesBlurred)
            self.labelCalibStart1.setText("")
            self.labelCalibCam1.setText("")
        except Exception as e:
            eMessage = "Failed to Finish Calibration \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.Stack.setCurrentIndex(4)

    def cancelCalib(self):
        try:
            self.labelCalibStart1.setText("")
            self.labelCalibCam1.setText("")
        except Exception as e:
            eMessage = "Failed to Cancel Calibration \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.Stack.setCurrentIndex(3)


    def startStream(self):
        """
        Kamera Stream wird gestartet und ausgegeben (Daheng)
        """
        try:
            prev_frame_time = np.zeros(len(self.cams))
            time_gap = np.zeros(len(self.cams))
            constant_fps = 0
            cam_stream_on(self.cams)
            while True:
                images = get_numpyImageBGR(self.cams)
                for i, cam in enumerate(self.cams):
                    # setting up fps counter with update
                    fps, prev_frame_time = get_frame_rate(prev_frame_time, i)  # returns int
                    fps = str(fps)
                    # updating fps every 500ms or so to display
                    constant_fps, time_gap = get_constant_framerate(fps, time_gap, constant_fps, i)
                    image = getStream(images, self.deviceManager, self.cams, constant_fps, i)
                    try:
                        img = resizeImg(image, (1100,500))
                        img = QPixmap.fromImage(img)
                        if i == 0:
                            self.labelStream.setPixmap(img)
                            self.labelStreamCalib.setPixmap(img)
                        #if i == 1:
                            #self.labelStream2.setPixmap(img)
                    except Exception as e:
                        print("Resizing Image failed \n" + str(e))
                time.sleep(0.1)
        except Exception as e:
            eMessage = "Starting Camera Stream (Daheng) failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def start_ImagesThread(self):
        #self.labelZoom.setHidden(True)
        #self.labelImage.setHidden(False)
        t = Timer(0.5, self.start_Images, args=())
        t.start()

    def start_Images(self):
        """
        Bilder werden aufgenommen und gespeichert (Daheng)
        """
        try:
            if self.comboBoxTrigger.currentText() == "automatisch":
                self.buttonBreak.setHidden(False)
                self.buttonTakePicture.setHidden(True)
            imgInfo = ["", self.comboBoxBBCH.currentText(), self.comboBoxCultivation.currentText()]
            sek = self.comboBoxInterval.currentText().split(" ")

            if self.comboBoxTrigger.currentText() == "manuell":
                loopEnd = 0
                self.labelCountdown.setHidden(True)
                lng = 0
                lat = 0
                """
                try:
                   lng, lat = func_timeout(2,getGPSData, args=())
                except:
                    eMessage = "No GPS Connection!!!"
                    print(eMessage)
                    writeLog("Error", eMessage)
                    lng = 0
                    lat = 0
                """

                self.GPSLng.append(lng)
                self.GPSLat.append(lat)

                try:
                    self.imageNames, self.imageData = make_Image(self.cams, self.labelPicturesNum, self.labelImage, self.labelImage2, self.imageNames, imgInfo, self.cameraStatus, self.imageData, self.tableDatasets, self.datasets)
                    #print("time4")
                    self.writeDataset()
                    writeRecoveryDataset(True, self.imageNames, self.imageData, self.GPSLat, self.GPSLng, self.settingsCamera, self.settingsDataset)
                    #print("time5")
                except Exception as e:
                    eMessage = "Image Making failed (Manuell) \n" + str(e)
                    print(eMessage)
                    writeLog("Error", eMessage)

                imgNum = self.labelPicturesNum.text().split(" ")
                #if imgNum[1] == imgNum[3]:
                    #self.buttonTakePicture.setEnabled(False)
            else:
                self.buttonComplete.setEnabled(False)
                self.buttonCancel.setEnabled(False)
                #self.buttonComplete.setStyleSheet("background-color: green; height: 100; color: grey")
                self.buttonCamera.setEnabled(False)
                loopEnd = int(self.textBoxMaxImages.text())
                self.labelCountdown.setText("-" + sek[0] + "-")
                self.labelCountdown.setHidden(False)
                t = Timer(0.5, self.make_Images, args=(loopEnd, int(sek[0]), imgInfo))
                t.start()
            #print("time6")
            self.checkImage()
            #print("time7")
        except Exception as e:
            eMessage = "Image Making failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        #print("time8")
        return None

    def checkImage(self):
        try:
            num = len(self.imageNames) - 1
            if num >= 0:
                img = cv2.imread("GUI_Data/" + self.imageNames[num] + ".jpg")
                blurry = ckeckImagesharpness(img, 100)
                #print(str(blurry))
                if blurry:
                    #self.show_new_window()
                    self.imagesBlurred = True
            #print(self.imagesBlurred)
        except Exception as e:
            eMessage = "Checking  Image sharpness failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)


    def zoomImage(self, type, fokus):

        try:
            image = None

            if type == "plus":
                self.imageZoom = self.imageZoom + 0.5
            elif type == "minus":
                if self.imageZoom > 1:
                    self.imageZoom = self.imageZoom - 0.5
                else:
                    self.imageZoom = 1
            else:
                self.imageZoom = 1
            if fokus:
                if self.fokusImage is not None:
                    image = self.fokusImage
                    image = cv2.resize(image, (1200,1077))
            else:
                if len(self.imageNames) > 0:
                    num = len(self.imageNames) - 1
                    path = Path_Images + self.imageNames[num] + ".jpg"
                    image = cv2.imread(path)
                    image = cv2.resize(image, (535,500))
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                zoomImage = clipped_zoom(image, self.imageZoom)
                zoomImage = qimage2ndarray.array2qimage(zoomImage)
                if fokus:
                    self.labelDahengStream.setPixmap(QPixmap.fromImage(zoomImage))
                else:
                    self.labelImage.setPixmap(QPixmap.fromImage(zoomImage))
        except Exception as e:
            eMessage = "Zooming Image failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)


    def updateTime(self):
        """
        Datum und Uhrzeit werden upgedatet und ausgegeben
        """
        batteryText = "Akku: "
        while self.GuiOn:
            try:
                now = QDateTime.currentDateTime()
                self.labelTime.setText(now.toString())
                battery = psutil.sensors_battery()
                battery = round(battery.percent)
                #self.labelBattery.setText(batteryText + str(battery) + "%")
                time.sleep(1)
            except Exception as e:
                eMessage = "Updating Time failed \n" + str(e)
                print(eMessage)
                writeLog("Error", eMessage)

    def switchImageStream(self, streamNum, button):
        """
        Wechsel zwischen Kamera Live-Stream und letztem Bild
        """
        try:
            bTextImage = "Letztes Bild"
            bTextStream = "Live Stream"
            if streamNum == 1:
                if button.text() == bTextStream:
                    self.labelImage.setHidden(True)
                    self.labelStream.setHidden(False)
                    button.setText(bTextImage)
                else:
                    self.labelStream.setHidden(True)
                    self.labelImage.setHidden(False)
                    button.setText(bTextStream)
            else:
                if button.text() == bTextStream:
                    self.labelImage2.setHidden(True)
                    self.labelStream2.setHidden(False)
                    button.setText(bTextImage)
                else:
                    self.labelStream2.setHidden(True)
                    self.labelImage2.setHidden(False)
                    button.setText(bTextStream)
        except Exception as e:
            eMessage = "Live-Stream/Camera switch failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def cancelRecording(self):
        """
        Bildaufnahme wird abgebrochen
        """
        self.Stack.setCurrentIndex(0)
        self.setRecordingStatus(False)
        try:
            self.imagesBlurred = False
            datasetNum = len(self.datasets) - 1
            deleteDatabaseDataset(self.datasets[datasetNum][0])
            self.datasets.pop()
        except Exception as e:
            eMessage = "Deleteting Dataset failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
        #writeDatasetData(self.datasets)
        try:
            for n in self.imageNames:
                imageName = Path_Images + n + ".jpg"
                fileName = Path_Images + n + ".json"
                try:
                    os.remove(imageName)
                except Exception as e:
                    eMessage = "Image could not be deleted \n" + str(e)
                    print(eMessage)
                    writeLog("Error", eMessage)
                try:
                    os.remove(fileName)
                except Exception as e:
                    eMessage = "File could not be deleted \n" + str(e)
                    print(eMessage)
                    writeLog("Error", eMessage)
            self.labelPicturesNum.setText("Bilder: 0 / " + self.textBoxMaxImages.text())
            self.uploadResponse = ""
            self.imageNames = []
            self.imageData = []
            self.GPSLat = []
            self.GPSLng = []
            self.labelPicturesNum.setText("Bilder: 0 / " + self.textBoxMaxImages.text())
            self.buttonBreak.setHidden(True)
            self.buttonResume.setHidden(True)
            self.buttonTakePicture.setHidden(False)
            self.buttonTakePicture.setEnabled(True)
            if self.autoImages:
                self.statusImageThread = False
            changeRecoveryDataset("status", False)
        except Exception as e:
            eMessage = "Failed to cancel Image making \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    """
    def startImageThread(self, num, interval, imgInfo):

        try:
            self.make_Images(num, interval, imgInfo)
        except Exception as e:
            eMessage = "Image making failed (automatic) \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
    """

    def make_Images(self, num, interval, imgInfo):
        """
        Macht in einem vorgegeneben abstand automatisch Bilder und gibt diese zurück
        """
        self.autoImages = True
        loop = 0
        try:
            while loop < num:
                self.labelCountdown.setText("-" + str(interval) + "-")
                i = interval
                time.sleep(1)
                while i > 0:
                    self.labelCountdown.setText("-" + str(i - 1) + "-")
                    time.sleep(1)
                    i = i - 1
                    while self.buttonBreak.isHidden() and self.statusImageThread:
                        time.sleep(1)
                        #print("sleep")
                        #print(self.statusImageThread)
                if self.statusImageThread:
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

                    self.GPSLng.append(lng)
                    self.GPSLat.append(lat)
                    self.imageNames, self.imageData = make_Image(self.cams, self.labelPicturesNum, self.labelImage, self.labelImage2, self.imageNames, imgInfo, self.cameraStatus, self.imageData, self.tableDatasets, self.datasets)
                    self.writeDataset()
                    writeRecoveryDataset(True, self.imageNames, self.imageData, self.GPSLat, self.GPSLng, self.settingsCamera, self.settingsDataset)
                    loop = loop + 1
                else:
                    loop = num
                    self.statusImageThread = True
            self.buttonComplete.setEnabled(True)
            self.buttonCancel.setEnabled(True)
            #self.buttonComplete.setStyleSheet("background-color: green; height: 100; color: white")
            self.buttonCamera.setEnabled(True)
            #self.buttonResume.setHidden(True)
            self.buttonBreak.setHidden(True)
            self.buttonTakePicture.setHidden(False)
            self.autoImages = False

        except Exception as e:
            eMessage = "Automatic Image making failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
            self.autoImages = False

        print("time6")
        return None


    def returnToCam(self):
        self.triggerImage(True)
        try:
            self.buttonCancelND.setHidden(False)
            self.buttonStartND.setHidden(False)
            self.buttonReturnND.setHidden(True)
            self.buttonDatasetND.setHidden(True)
            self.labelNotice.hide()
        except Exception as e:
            eMessage = "Going back to Camera failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.Stack.setCurrentIndex(4)

    def endDataset(self):
        """
        Datensatz wird abgeschlossen und Hochgeladen
        """
        self.setRecordingStatus(False)
        try:
            updateTable(self.tableDatasets, 1, self.comboBoxCultivation.currentText(), self.datasets)
            updateTable(self.tableDatasets, 2, self.comboBoxBBCH.currentText(), self.datasets)
            updateTable(self.tableDatasets, 3, self.comboBoxLight.currentText(), self.datasets)
            updateTable(self.tableDatasets, 4, self.comboBoxGround.currentText(), self.datasets)
            self.labelNoticeUpload.show()
            self.buttonUpload.setEnabled(False)
            #self.buttonUpload.setStyleSheet("background-color: grey; height: 100")
            self.writeDataset()
            self.labelPicturesNum.setText("Bilder: 0 / " + self.textBoxMaxImages.text())
            t = Timer(1.0, dataUpload, args=(self.imageNames, self.datasets, self.tableDatasets, 0, self.labelNoticeUpload, self.buttonUpload, False, False, self.settingAdmin[7]))
            t.start()
            writeLog("upload", "")
            self.datasetNum = self.datasetNum + 1
            self.imagesNum =  self.imagesNum + len(self.imageNames)
            self.imageNames = []
            self.imageData = []
            self.GPSLat = []
            self.GPSLng = []
            self.uploadResponse = ""
            self.imagesBlurred = False
            changeRecoveryDataset("status", False)

            if self.autoImages:
                self.statusImageThread = False

            self.buttonCancelND.setHidden(False)
            self.buttonStartND.setHidden(False)
            self.buttonReturnND.setHidden(True)
            self.buttonDatasetND.setHidden(True)

            self.buttonBreak.setHidden(True)
            self.buttonTakePicture.setHidden(False)
            self.buttonTakePicture.setEnabled(True)
            self.labelNotice.hide()
            writeDatasetNum(self.datasetNum, self.imagesNum, self.datasetsDate)
            logText = "Datesets: " + str(self.datasetNum) + " Images: " + str(self.imagesNum)
            writeLog("DatasetsNum", logText)
        except Exception as e:
            eMessage = "Finish dataset failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.Stack.setCurrentIndex(0)
        #self.buttonDatasetND.setText("Datensatz abschließen und hochladen")

    def startUploadThread(self):
        #self.checkBoxCheckedNum = 0
        #self.uploadWindow = UploadWindow()
        self.buttonDeleteST.setStyleSheet("background-color: red; height: 100; color: white")
        t = Timer(1.0, self.uploadSelectedDataset, args=())
        t.start()

    def uploadSelectedDataset(self):
        """
        Ausgewählter Datensatz wird Hochgeladen
        """

        try:
            self.buttonUpload.setEnabled(False)
            #self.buttonUpload.setStyleSheet("background-color: grey; height: 100; color: white")
            tableRow = 0
            tableRowNum = len(self.datasets) - 1
            dataset = len(self.datasets) - 1
            while tableRow <= tableRowNum:
                if self.tableDatasets.item(tableRow,7).checkState() == Qt.Checked:
                    self.labelNoticeUpload.show()
                    print("Upload Datensatz: " + self.datasets[dataset][0])
                    dataUpload(self.datasets[dataset][9], self.datasets, self.tableDatasets, tableRow, self.labelNoticeUpload, self.buttonUpload, True, False, self.settingAdmin[7])
                    self.tableDatasets.item(tableRow,7).setCheckState(Qt.Unchecked)
                tableRow = tableRow + 1
                dataset = dataset - 1
            self.buttonDeleteST.setEnabled(True)
            self.checkBoxUploadedNum = 0
            self.checkBoxCheckedNum = 0
        except Exception as e:
            eMessage = "Uploading selected Dataset failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
        self.buttonUpload.setEnabled(True)
        #self.buttonUpload.setStyleSheet("background-color: green; height: 100; color: white")

    def deleteSelectedDataset(self):
        """
        Ausgewählter Datensatz wird gelöscht
        """
        try:
            self.buttonUpload.setEnabled(True)
            self.buttonUpload.setStyleSheet("background-color: green; height: 100; color: white")
            self.checkBoxUploadedNum = 0
            tableRow = 0
            tableRowNum = len(self.datasets) - 1
            dataset = len(self.datasets) - 1
            while tableRow <= tableRowNum:
                if self.tableDatasets.item(tableRow,7).checkState() == Qt.Checked:
                    self.tableDatasets.removeRow(tableRow)
                    i = tableRowNum - tableRow
                    deleteDatabaseDataset(self.datasets[i][0])
                    for n in self.datasets[i][9]:
                        imageName = Path_Images + n + ".jpg"
                        fileName = Path_Images + n + ".json"
                        try:
                            os.remove(imageName)
                        except Exception as e:
                            eMessage = "Image could not be deleted \n" + str(e)
                            print(eMessage)
                            writeLog("Error", eMessage)
                        try:
                            os.remove(fileName)
                        except Exception as e:
                            eMessage = "File could not be deleted \n" + str(e)
                            print(eMessage)
                            writeLog("Error", eMessage)
                    while i < tableRowNum:
                        self.datasets[i] = self.datasets[i + 1]
                        i = i + 1
                    self.datasets.pop()
                    tableRowNum = tableRowNum - 1
                    tableRow = tableRow - 1
                tableRow = tableRow + 1
                dataset = dataset - 1
            #writeDatasetData(self.datasets)
        except Exception as e:
            eMessage = "Deleting selected Dataset failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.Stack.setCurrentIndex(0)

    def checkTriggerChange(self):

        if self.comboBoxTrigger.currentText() == "manuell":
            self.comboBoxInterval.setEnabled(False)
            self.buttonTakePicture.setHidden(False)
            self.buttonBreak.setHidden(True)
            self.buttonResume.setHidden(True)
            self.labelTriggerText.setText("Manuel Auslösung")
            if self.autoImages:
                self.statusImageThread = False
        else:
            self.comboBoxInterval.setEnabled(True)
            #self.buttonTakePicture.setHidden(True)
            #self.buttonBreak.setHidden(False)
            #self.buttonResume.setHidden(True)
            self.labelTriggerText.setText("Auto Auslösung")


    def checkPin(self):
        """
        Pin Input wird überprüft
        """
        try:
            if self.textBoxPIN.text() != "":
                input = self.textBoxPIN.text()
                newKey = encryptPin(input, self.pinSalt)

                if newKey == self.pinKey:
                    self.Stack.setCurrentIndex(6)
                    deleteText(self.textBoxPIN)
        except Exception as e:
            eMessage = "Checking PIN failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def endRecording(self):
        """
        Fotoaufnahme wird abgeschlossen
        """
        self.triggerImage(False)
        try:
            self.buttonCancelND.setHidden(True)
            self.buttonStartND.setHidden(True)
            self.buttonReturnND.setHidden(False)
            self.buttonDatasetND.setHidden(False)

            textNum = self.labelPicturesNum.text().split(":")
            num = textNum[1].split("/")
            self.writeDataset()
            if int(num[0]) < int(num[1]):
                self.labelNotice.show()
                self.labelNotice.setText("!Hinweis! Datensatz nicht \n vollständig: (Bilder:" + textNum[1] + ")")
            if self.imagesBlurred:
                self.show_new_window()
        except Exception as e:
            eMessage = "Finish Image making failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.Stack.setCurrentIndex(3)

    def checkText(self, num, box, disabledButton1, disabledButton2):
        try:
            if num != 5:
                text = box.currentText()
            elif num == 5:
                text = box.text()
            if text == "":
                self.textIsSet[num] = False
            else:
                self.textIsSet[num] = True

            n = 0
            allBoxTextIsSet = True
            while n < 6:
                if self.textIsSet[n] == False:
                    allBoxTextIsSet = False
                n = n + 1

            if allBoxTextIsSet:
                disabledButton1.setEnabled(True)
                disabledButton1.setStyleSheet("background-color: green; height: 100; color: white")
                disabledButton2.setEnabled(True)
                disabledButton2.setStyleSheet("background-color: green; height: 100; color: white")
            else:
                disabledButton1.setEnabled(False)
                disabledButton1.setStyleSheet("background-color: grey; height: 100; color: white")
                disabledButton2.setEnabled(False)
                disabledButton2.setStyleSheet("background-color: grey; height: 100; color: white")
        except Exception as e:
            eMessage = "Checking text failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def increaseExposure(self, textbox):
        exposure = textbox.text()
        exposure = int(exposure) + 20
        if exposure >= 1000:
            exposure = 1000
        textbox.setText(str(exposure))

    def decreaseExposure(self, textbox):
        exposure = textbox.text()
        exposure = int(exposure) - 20
        if exposure <= 40:
            exposure = 40
        textbox.setText(str(exposure))

    def openDatasetWidget(self):

        self.buttonReturnND2.setHidden(False)
        self.buttonSaveND.setHidden(False)
        self.buttonCancelND.setHidden(True)
        self.buttonStartND.setHidden(True)

        self.Stack.setCurrentIndex(3)

    def checkBoxChanged(self, row, column):
        try:
            #print("Eingang checkBox: " + str(self.checkBoxUploadedNum))
            #print("Eingang checkBox2: " + str(self.checkBoxCheckedNum))
            item = self.tableDatasets.item(row, column)
            if item is not None:
                if column == 7:
                    if self.tableDatasets.item(row, 6).text() == "fehlgeschlagen" or self.tableDatasets.item(row, 6).text() == "unvollständig":
                        if item.checkState() == Qt.Checked:
                            self.checkBoxCheckedNum = self.checkBoxCheckedNum + 1
                            self.buttonDeleteST.setEnabled(False)
                            self.buttonDeleteST.setStyleSheet("background-color: grey; height: 100; color: white")
                        else:
                            if self.checkBoxCheckedNum >= 1:
                                self.checkBoxCheckedNum = self.checkBoxCheckedNum - 1
                            if self.checkBoxCheckedNum == 0:
                                self.buttonDeleteST.setEnabled(True)
                                self.buttonDeleteST.setStyleSheet("background-color: red; height: 100; color: white")

                    elif self.tableDatasets.item(row, 6).text() == "vollständig":
                        if item.checkState() == Qt.Checked:
                            self.checkBoxUploadedNum = self.checkBoxUploadedNum + 1
                            self.buttonUpload.setEnabled(False)
                            self.buttonUpload.setStyleSheet("background-color: grey; height: 100; color: white")
                        else:
                            if self.checkBoxUploadedNum >= 1:
                                self.checkBoxUploadedNum = self.checkBoxUploadedNum - 1
                            if self.checkBoxUploadedNum == 0:
                                self.buttonUpload.setEnabled(True)
                                self.buttonUpload.setStyleSheet("background-color: green; height: 100; color: white")

            #print("checkBox: " + str(self.checkBoxUploadedNum))
            #print("checkBox2: " + str(self.checkBoxCheckedNum))
        except Exception as e:
            eMessage = "Checking Checkbox failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def startELogThread(self):

        self.labelEStatus.show()
        self.buttonSendLogs.setEnabled(False)
        tELog = Timer(0, self.sendLogFiles, args=())
        tELog.start()


    def sendLogFiles(self):

        try:
            tableRow = 0
            tableRowNum = len(self.logfiles) - 1
            while tableRow <= tableRowNum:
                if self.tableLogs.item(tableRow,2).checkState() == Qt.Checked:
                    filename = self.tableLogs.item(tableRow, 1).text()
                    file = Path_Log_Files + filename
                    text = "Sending LogFile " + filename + "\n" + self.comboBoxDevice.currentText() + " " + self.comboBoxSensor.currentText()
                    subject = "Sending Logfile"
                    print(file)
                    emailWithFile(Email_Receiver_Logs, subject, text, file)
                    self.tableLogs.item(tableRow,2).setCheckState(Qt.Unchecked)
                tableRow = tableRow + 1
        except Exception as e:
            eMessage = "Sending E-Mail failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.labelEStatus.hide()
        self.buttonSendLogs.setEnabled(True)

    def sendDatasetNum(self):

        eSuccess = True
        print("Sending E-Mail")
        try:
            deviceText = self.comboBoxDevice.currentText().split(" ")
            if len(deviceText) >= 2:
                deviceNum = deviceText[1] 
            else:
                deviceNum = ""
            sensorText = self.comboBoxSensor.currentText().split(" ")
            if len(sensorText) >= 2:
                sensorNum = sensorText[1]
            else:
                sensorNum = ""
            eSubject = "Datensatz Zählung Handwagen (Automatisch)"
            eText = "Anzahl der erstellten Datensätze und aufgenommenen Bilder.\n\n" \
                    + "Zeitraum:                  " + self.datasetsDate + " - " + (datetime.now()).strftime('%a. %b %d %X %Y') + "\n" \
                    + "Handgerät:               " + deviceNum + "\n" \
                    + "Sensorbox:               " + sensorNum + "\n" \
                    + "Anzahl Datensätze:  " + str(self.datasetNum) + "\n" \
                    + "Anzahl Bilder:           " + str(self.imagesNum)
            
        
            emailTextonly(Email_Receiver_DataNum, eSubject, eText)
        except Exception as e:
            eSuccess = False
            eMessage = "Sending E-Mail failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        if eSuccess:
            self.datasetNum = 0
            self.imagesNum = 0
            self.datasetsDate = datetime.now()
            self.datasetsDate = self.datasetsDate.strftime('%a. %b %d %X %Y')
            writeDatasetNum(self.datasetNum, self.imagesNum, self.datasetsDate)



    def addNewDataset(self):
        try:
            time = datetime.now()

            textNum = self.labelPicturesNum.text().split(":")

            chkBoxSelection = QTableWidgetItem()
            chkBoxSelection.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxSelection.setCheckState(Qt.Unchecked)

            newdataset = [time.strftime('%a. %b %d %X %Y'), "", self.comboBoxCultivation.currentText(), self.comboBoxBBCH.currentText(),
            self.comboBoxLight.currentText(), self.comboBoxGround.currentText(), textNum[1], self.uploadResponse, chkBoxSelection, self.imageNames, []]

            addDatabaseDataset(newdataset)

            #self.datasetNames = self.imageNames

            self.datasets.append(newdataset)

            row = len(self.datasets) - 1
            #setData(self.tableDatasets, self.datasets)
            addData(self.tableDatasets, self.datasets[row], row)

            #self.checkBoxCheckedNum = self.checkBoxCheckedNum + 1

        except Exception as e:
            eMessage = "Adding new Dataset failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def recoverRecording(self):
        """
        Abgebrochene Aufnahme wird wieder hergestellt
        """

        try:
            self.setRecordingStatus(True)
            self.triggerImage(True)
            imageNum = len(self.imageNames)
            self.labelPicturesNum.setText("Bilder: " + str(imageNum) + " / " + self.textBoxMaxImages.text())
            self.setDatasetValues()
            self.setCameraSettings()
        except Exception as e:
            eMessage = "Recovering last Recording failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

        self.Stack.setCurrentIndex(4)



    def writeDataset(self):
        """
        Neuer Datensatz wird erstellt und gespeichert
        """

        try:
            n = 0
            deviceText = (self.comboBoxDevice.currentText()).split(" ")
            deviceNum = "device_number-" + deviceText[1]
            sensorText = (self.comboBoxSensor.currentText()).split(" ")
            sensorNum =  "sensorbox_number-" + sensorText[1]
            while n < len(self.imageNames):
                dataInput = [self.comboBoxCultivation.currentText(), self.comboBoxLight.currentText(), self.comboBoxBBCH.currentText(),
                self.comboBoxGround.currentText(), self.comboBoxInfluences.currentIndex(), self.comboBoxInfestation.currentIndex(),
                self.comboBoxDistance.currentText(), self.GPSLng[n], self.GPSLat[n], self.textBoxType.text(), sensorNum,
                deviceNum]
                writeData(dataInput, self.imageNames[n], self.imageData[n], self.settingAdmin[7])
                n = n + 1
        except Exception as e:
            eMessage = "Saving Dataset failed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)

    def getCamStatus(self):

        statusDaheng = "1"
        while self.GuiOn:
            try:
                daheng = getCameraData("status", "Cam_1")
                if daheng != statusDaheng:
                    if daheng == "1":
                        self.labelCam1.setStyleSheet("background-color: green; color: white")
                    elif daheng == "0":
                        self.labelCam1.setStyleSheet("background-color: red; color: white")
                    else:
                        print("Getting Camera Status failed (Daheng)")
                statusDaheng = daheng
                time.sleep(3)

            except Exception as e:
                eMessage = "Getting Camera Status failed \n" + str(e)
                print(eMessage)
                writeLog("Error", eMessage)
                time.sleep(5)

    def getTrigger(self):
        """
        Informationen zum Manuellen Trigger werden zurückgegeben
        """
        connected = False
        while self.GuiOn:
            try:
                mydb = mysql.connector.connect(
                  host="localhost",
                  user="ailand",
                  password="etarob",
                  database="handwagen"
                )
                mycursur = mydb.cursor()
                n = 0
                #try:
                mycursur.execute("SELECT hard_capture FROM control")

                myresult = mycursur.fetchall()
                mydb.commit()
                for x in myresult:
                    text = str(x)
                    result = str(x).split(",")
                    result = result[0].split("(")
                    if result[1] == "1":
                        mycursur.execute("SELECT soft_capture FROM control")

                        myresult = mycursur.fetchall()
                        mydb.commit()
                        for x in myresult:
                            text = str(x)
                            result = str(x).split(",")
                            result = result[0].split("(")
                            if result[1] == "0":
                                #mycursur.execute("UPDATE control SET soft_capture = '1' WHERE 1")
                                #mydb.commit()
                                if self.imgMaking == True and self.comboBoxTrigger.currentText() == "manuell":
                                    self.start_Images()
                time.sleep(0.2)
                #except Exception as e:
                    #print("Trigger Signal entnahme aus Datenbank fehlgeschlagen \n" + str(e))
            except Exception as e:
                eMessage = "Getting Trigger Signal failed \n" + str(e)
                print(eMessage)
                writeLog("Error", eMessage)
                time.sleep(1)


    def closeEvent(self, event):
        try:
            self.GuiOn = False
        except:
            print("Closing Threads failed")

        try:
            if self.infoWindow:
                self.infoWindow.close()
        except:
            print("Closing additonal Window failed")





def main():
    app = QApplication([])
    window = test()
    window.setWindowIcon(QIcon(Path_GUI_Icon))
    #window.show()
    window.showMaximized()
    app.exec_()



if __name__ == "__main__":
    main()

    #sys.exit(app.exec_())
