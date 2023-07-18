import json
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from log import *

Path_Admin_Settings = "/home/ailand/GUI_Data/Data/AdminSettings.json"
Path_Camera_Settings = "/home/ailand/GUI_Data/Data/CameraSettings.json"

def writeAdminSetting(data):
    """
    Übergebene Admin Einstellungen werden im json Format gespeichert
    """

    datasets = {}

    datasets["Einstellungen"] = []
    #for i in data:

    element = {
    "Language": data[0],
    "Device": data[1],
    "Sensorbox": data[2],
    "Upload": data[3],
    "CamStatus1": data[4],
    "CamStatus2": data[5],
    "MaxImages": data[6],
    "Server": data[7],
    }
    datasets["Einstellungen"].append(element)

    # Serializing json
    json_object = json.dumps(datasets, indent=4)

    # Writing to sample.json
    try:
        with open(Path_Admin_Settings, "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        eMessage = "Admin Settings could not be saved \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def readAdminSettings():
    """
    Admin Einstellungen werden aus einer json Datei gelesen und zurückgegeben
    """
    datasets = []

    with open(Path_Admin_Settings, 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)
        #for i in json_object['Einstellungen']:
        settings = json_object['Einstellungen'][0]

        data = [ settings['Language'], settings['Device'], settings['Sensorbox'], settings['Upload'], settings['CamStatus1'], settings['CamStatus2'], settings['MaxImages'], settings['Server']]

        return data

def writeCamSettings(data):
    """
    Übergebene Datensätze werden im json Format gespeichert
    """
    datasets = {}
    datasets["Einstellungen"] = []

    element = {
    "Trigger": data[0],
    "Interval": data[1],
    "ExposTime1": data[2],
    "ExposTime2": data[3],
    }
    datasets["Einstellungen"].append(element)


    # Serializing json
    json_object = json.dumps(datasets, indent=4)

    # Writing to sample.json
    try:
        with open(Path_Camera_Settings, "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        eMessage = "Dataset Data could not be saved \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def readCamSettings():
    """
    Admin Einstellungen werden aus einer json Datei gelesen und zurückgegeben
    """
    datasets = []

    with open(Path_Camera_Settings, 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)
        #for i in json_object['Einstellungen']:
        settings = json_object['Einstellungen'][0]

        data = [ settings['Trigger'], settings['Interval'], settings['ExposTime1'], settings['ExposTime2']]

        return data

