import json
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from log import *

Path_Last_Dataset = "/home/ailand/GUI_Data/Data/lastDataset.json"

def writeRecoveryDataset(recStatus, ImageNames, ImageData, GPSLat, GPSLng, CameraSettings, datasetData):
    """
    Speichert denn Datensatz für denn fall eines Systemabsturzes oder ungewohlte beendigung
    der GUI.
    """

    dataset = {}

    dataset["Status"] = []
    dataset["Data"] = []
    dataset["Settings"] = []
    dataset["Dataset"] = []

    status = {
    "Status": recStatus,
    }

    dataset["Status"].append(status)

    data = {
    "ImageNames": ImageNames,
    "ImageData": ImageData,
    "GPSLat": GPSLat,
    "GPSLng": GPSLng,
    }
    dataset["Data"].append(data)

    settings = {
    "Setting": CameraSettings,
    }
    dataset["Settings"].append(settings)

    datasetData = {
    "Dataset": datasetData,
    }
    dataset["Dataset"].append(datasetData)


    # Serializing json
    json_object = json.dumps(dataset, indent=4)

    # Writing to sample.json
    try:
        with open(Path_Last_Dataset, "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        eMessage = "Recovery dataset data could not be saved \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def readRecoveryDataset():
    """
    Admin Einstellungen werden aus einer json Datei gelesen und zurückgegeben
    """

    with open(Path_Last_Dataset, 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)
        #for i in json_object['Einstellungen']:
        status = json_object['Status'][0]
        data = json_object['Data'][0]
        settings = json_object['Settings'][0]
        dataset = json_object['Dataset'][0]

        recordstatus = status['Status']
        ImageNames = data["ImageNames"]
        ImageData = data["ImageData"]
        GPSLat = data["GPSLat"]
        GPSLng = data["GPSLng"]
        setting = settings["Setting"]
        datasetData = dataset["Dataset"]

        return recordstatus, ImageNames, ImageData, GPSLat, GPSLng, setting, datasetData

def changeRecoveryDataset(value, data):

    try:
        recordstatus, ImageNames, ImageData, GPSLat, GPSLng, setting, datasetData = readRecoveryDataset()

        if  value == "status":
            recordstatus = data
        elif value == "setting":
            setting = data
        elif value == "dataset":
            datasetData = data

        writeRecoveryDataset(recordstatus, ImageNames, ImageData, GPSLat, GPSLng, setting, datasetData)
    except Exception as e:
        eMessage = "Recovery dataset value could not be changed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)







