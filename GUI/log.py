# This Python file uses the following encoding: utf-8
from datetime import datetime
import json
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

Path_Log_Files = "/home/ailand/GUI_Data/logs/"
Path_Log_Data = "/home/ailand/GUI_Data/Data/logs.json"

def writeLog(type, info):
    """
    Übergebener Log wird in eine Datei geschrieben
    """

    fileName = datetime.now().strftime('%d_%m_%Y_') + "logfile.log"
    file = Path_Log_Files + fileName

    text = ""
    if type == "login":
        text = "User login " + info
    if type == "image":
        text = "Image Made " + info
    if type == "upload":
        text = "Upload Dataset " + info
    if type == "imageInfo":
        text = "Image Info " + info
    if type == "DatasetsNum":
        text = "Dataset Completed " + info
    if type == "Error":
        text = "Error " + info

    #print("Info: " + info)
    #print("Text: " + text)

    try:
        with open(file, "a") as outfile:
            outfile.write("\n" + datetime.now().strftime('%a %d %b %X %Y ') + text)
    except Exception as e:
        print("New Log Entry could not be saved \n" + str(e))

def writeLogs(logs):
    """
    Übergebene Log Datei Namen werden im json Format in eine Datei geschrieben
    """

    data = {}
    data["Logs"] = []
    for i in logs:
        data["Logs"].append(i)

    json_object = json.dumps(data, indent=4)
    try:
        with open(Path_Log_Data, "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        print("Log File Names could not be saved \n" + str(e))


def readLogs():
    """
    Log Datei Namen der einer json Datei entnommen und zurückgegeben
    """

    logs = []
    try:
        with open(Path_Log_Data, 'r') as openfile:

            # Reading from json file
            json_object = json.load(openfile)
            for i in json_object['Logs']:
                logs.append(i)
    except Exception as e:
        print("Log Files could not be read \n" + str(e))

    try:
        fileName = datetime.now().strftime('%d_%m_%Y_') + "logfile.log"

        if len(logs) >= 1:
            lognum = len(logs) - 1
            if logs[lognum] != fileName:
                logs.append(fileName)
        else:
            logs.append(fileName)

        writeLogs(logs)

    except Exception as e:
        print("Log File Names could not be saved \n" + str(e))

    return logs


def setLogData(table, data):
    """
    Übergebene Log Datei Informationen werden in die Tabelle eingetragen
    """

    for i in data:

        table.insertRow(0);

        filename = i.split("_")
        date = filename[0] + " " + filename[1] + " " + filename[2]

        itemDate = QTableWidgetItem()
        itemDate.setText(date)
        table.setItem(0,0,itemDate)

        itemName = QTableWidgetItem()
        itemName.setText(i)
        table.setItem(0,1,itemName)

        chkBoxSelection = QTableWidgetItem()
        chkBoxSelection.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chkBoxSelection.setCheckState(Qt.Unchecked)
        table.setItem(0,2,chkBoxSelection)
