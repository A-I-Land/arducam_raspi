import json
import os
import subprocess
import mysql.connector
from log import *
from datetime import datetime
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

lightEn = {
    "sonnig": "sunny",
    "bewölkt": "cloudy",
    "dämmrig": "crepuscular",
    "dunkel": "dark"
}
groundEn = {
    "trocken": "dry",
    "feucht": "wet",
    "übergang": "transition"
}
cultivationId = {
    "Weizen": "df987497-fed6-47da-b506-8124d74a23c0",
    "Gerste": "df987497-fed6-47da-b506-8124d74a23c0",
    "Raps": "df987497-fed6-47da-b506-8124d74a23c0",
    "Mais": "df987497-fed6-47da-b506-8124d74a23c0",
    "Zuckerrübe": "df987497-fed6-47da-b506-8124d74a23c0",
    "Kartoffel": "df987497-fed6-47da-b506-8124d74a23c0",
    "Soja": "df987497-fed6-47da-b506-8124d74a23c0",
    "Sonnenblume": "df987497-fed6-47da-b506-8124d74a23c0",
    "Stoppel": "96a1041b-e149-4b61-820a-c796130dc521",
    "Grünland": "3e5cfcf3-42f2-4598-9a0d-bb2b3670cdf3",
    "Erbse": "fbbfece8-7baa-485c-a852-07b87d0ff3b9",
    "Ackerbohne": "fbbfece8-7baa-485c-a852-07b87d0ff3b9",
    "Boden": "01496065-345d-4f63-a21f-4163bb6cbf88"
}

cultivationIdProd = {
    "Weizen": "df987497-fed6-47da-b506-8124d74a23c0",
    "Gerste": "df987497-fed6-47da-b506-8124d74a23c0",
    "Raps": "df987497-fed6-47da-b506-8124d74a23c0",
    "Mais": "df987497-fed6-47da-b506-8124d74a23c0",
    "Zuckerrübe": "df987497-fed6-47da-b506-8124d74a23c0",
    "Kartoffel": "df987497-fed6-47da-b506-8124d74a23c0",
    "Soja": "df987497-fed6-47da-b506-8124d74a23c0",
    "Sonnenblume": "df987497-fed6-47da-b506-8124d74a23c0",
    "Stoppel": "a3897e5b-4115-4b20-9399-b9ef7c939eec",
    "Grünland": "a1814519-f88d-4214-8bdf-58d7918cf745",
    "Erbse": "fbbfece8-7baa-485c-a852-07b87d0ff3b9",
    "Ackerbohne": "fbbfece8-7baa-485c-a852-07b87d0ff3b9",
    "Boden": "3bcc9a60-01fb-4c6c-ba6d-992471c13916"
}

scopeId = {
    "Weizen": "75616b61-2300-4d22-a77a-ada74e176813",
    "Gerste": "75616b61-2300-4d22-a77a-ada74e176813",
    "Raps": "75616b61-2300-4d22-a77a-ada74e176813",
    "Mais": "75616b61-2300-4d22-a77a-ada74e176813",
    "Zuckerrübe": "75616b61-2300-4d22-a77a-ada74e176813",
    "Kartoffel": "75616b61-2300-4d22-a77a-ada74e176813",
    "Soja": "75616b61-2300-4d22-a77a-ada74e176813",
    "Sonnenblume": "75616b61-2300-4d22-a77a-ada74e176813",
    "Stoppel": "809faf53-b7bc-4ac5-90e6-21334dd00ed6",
    "Grünland": "809faf53-b7bc-4ac5-90e6-21334dd00ed6",
    "Erbse": "75616b61-2300-4d22-a77a-ada74e176813",
    "Ackerbohne": "75616b61-2300-4d22-a77a-ada74e176813",
    "Boden": "809faf53-b7bc-4ac5-90e6-21334dd00ed6"
}

scopeIdProd = {
    "Weizen": "75616b61-2300-4d22-a77a-ada74e176813",
    "Gerste": "75616b61-2300-4d22-a77a-ada74e176813",
    "Raps": "75616b61-2300-4d22-a77a-ada74e176813",
    "Mais": "75616b61-2300-4d22-a77a-ada74e176813",
    "Zuckerrübe": "75616b61-2300-4d22-a77a-ada74e176813",
    "Kartoffel": "75616b61-2300-4d22-a77a-ada74e176813",
    "Soja": "75616b61-2300-4d22-a77a-ada74e176813",
    "Sonnenblume": "75616b61-2300-4d22-a77a-ada74e176813",
    "Stoppel": "37afc7f8-d870-4a0b-8324-8d05b06c87c8",
    "Grünland": "37afc7f8-d870-4a0b-8324-8d05b06c87c8",
    "Erbse": "75616b61-2300-4d22-a77a-ada74e176813",
    "Ackerbohne": "75616b61-2300-4d22-a77a-ada74e176813",
    "Boden": "37afc7f8-d870-4a0b-8324-8d05b06c87c8"
}

type1 = {
    "Weizen": "code",
    "Gerste": "code",
    "Raps": "code",
    "Mais": "code",
    "Zuckerrübe": "code",
    "Kartoffel": "code",
    "Soja": "code",
    "Sonnenblume": "code",
    "Stoppel": "customdata",
    "Grünland": "customdata",
    "Erbse": "code",
    "Ackerbohne": "code",
    "Boden": "customdata"
}

type2 = {
    "Weizen": "croptype",
    "Gerste": "croptype",
    "Raps": "croptype",
    "Mais": "croptype",
    "Zuckerrübe": "croptype",
    "Kartoffel": "croptype",
    "Soja": "croptype",
    "Sonnenblume": "croptype",
    "Stoppel": "customitem",
    "Grünland": "customitem",
    "Erbse": "croptype",
    "Ackerbohne": "croptype",
    "Boden": "customitem"
}

codeId = {
    "Weizen": "3526546f-90d6-4158-8b9e-4a3ab1fe802f",
    "Gerste": "35ddf28d-0cfa-448f-9981-bfd392794bab",
    "Raps": "f355498c-d92d-41eb-947d-e0ca3e3853f3",
    "Mais": "0fddf53a-07c6-481a-8ac6-b48ea22e9dad",
    "Zuckerrübe": "0bf07efe-3f7a-46bb-86b7-144c870ab0d3",
    "Kartoffel": "2b74bb29-12f5-48af-9486-7e44e2fce900",
    "Soja": "8200d26b-41de-40cf-9e1d-a973413960f6",
    "Sonnenblume": "d6efa10b-6df1-4ebd-a049-45e1d13e46a1",
    "Stoppel": "22df9292-3931-4074-bba3-654a939acc11",
    "Grünland": "22df9292-3931-4074-bba3-654a939acc11",
    "Erbse": "51b260f4-1201-4bbe-8716-19520d19c5f9",
    "Ackerbohne": "9518dcee-c74c-42ec-a18f-d107cbf23e2e",
    "Boden": "22df9292-3931-4074-bba3-654a939acc11"
}
codeIdProd = {
    "Weizen": "3526546f-90d6-4158-8b9e-4a3ab1fe802f",
    "Gerste": "35ddf28d-0cfa-448f-9981-bfd392794bab",
    "Raps": "f355498c-d92d-41eb-947d-e0ca3e3853f3",
    "Mais": "0fddf53a-07c6-481a-8ac6-b48ea22e9dad",
    "Zuckerrübe": "0bf07efe-3f7a-46bb-86b7-144c870ab0d3",
    "Kartoffel": "2b74bb29-12f5-48af-9486-7e44e2fce900",
    "Soja": "8200d26b-41de-40cf-9e1d-a973413960f6",
    "Sonnenblume": "d6efa10b-6df1-4ebd-a049-45e1d13e46a1",
    "Stoppel": "1a1b75e4-f857-406f-8082-e4c2d7cac11e",
    "Grünland": "1a1b75e4-f857-406f-8082-e4c2d7cac11e",
    "Erbse": "51b260f4-1201-4bbe-8716-19520d19c5f9",
    "Ackerbohne": "9518dcee-c74c-42ec-a18f-d107cbf23e2e",
    "Boden": "1a1b75e4-f857-406f-8082-e4c2d7cac11e"
}

Influences = ["","Mechanical damage", "Leaf color", "Heat", "Water", "Phytotox", "Herbicide damage"]
Infestation = ["", "Thistle", "Heavy weed pressure", "No weed pressure"]
Path_Dataset_Num = "/home/ailand/GUI_Data/Data/DatasetsNum.json"
Path_GPS_Settings = "/home/ailand/setup_gps/setup_gps.sh.x"
Path_GPS_Command = "/home/ailand/setup_gps/get_gps.sh.x"
Path_Upload_Skript = "sh /home/ailand/GUI_Data/"
Path_Image_Files = "GUI_Data/"

def writeData(data, imgName, imageData, server):
    """
    Übergebene Daten werden im json Format gespeichert
    """
    try:
        name = imgName.split("/")
        fileName = name[1].split("_")
        #date = fileName[0].split("-")
        time = fileName[1].split("-")
        dateTime = fileName[0] + "T" + time[0] + ":" + time[1] + ":" + time[2] + "Z"
        jsonData = makeJsonData(data, dateTime, imageData, server)
        json_object = json.dumps(jsonData, indent=4)

        fileName = Path_Image_Files + imgName + ".json"
        try:
            with open(fileName, "w") as outfile:
                outfile.write(json_object)
        except Exception as e:
            eMessage = "Json File could not be saved \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
    except Exception as e:
        eMessage = "Dataset could not be saved \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)


def writeDatasetData(data):
    """
    Übergebene Datensätze werden im json Format gespeichert
    """
    datasets = {}
            #"Datensatz":
          # }
    #i = len(data)
    #element = []
    datasets["Datensatz"] = []
    for i in data:

        #images = ""
        #for k in i[9]:
            #images = images +

        element = {
        "Time": i[0],
        "Business": i[1],
        "Cultivation": i[2],
        "BBCH": i[3],
        "Light": i[4],
        "Ground": i[5],
        "ImageNum": i[6],
        "Upload": i[7],
        }
        datasets["Datensatz"].append(element)

    h = 0
    for k in datasets["Datensatz"]:
        k["Images"] = []
        for j in data[h][9]:
            k["Images"].append(j)
        h = h + 1

    l = 0
    for m in datasets["Datensatz"]:
        m["UploadImages"] = []
        if len(data[l]) >= 11:
            for n in data[l][10]:
                m["UploadImages"].append(n)
        l = l + 1


    # Serializing json
    json_object = json.dumps(datasets, indent=4)

    # Writing to sample.json
    try:
        with open("/home/ailand/GUI/Data/Datasets.json", "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        eMessage = "Dataset Data could not be saved \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)


def writeDatasetNum(num, images, date):
    """
    Übergebene Datensätze werden im json Format gespeichert
    """
    datasets = {}
    datasets["Datensatz"] = []

    element = {
    "Date": date,
    "Number": num,
    "Images": images,
    }
    datasets["Datensatz"].append(element)


    # Serializing json
    json_object = json.dumps(datasets, indent=4)

    # Writing to sample.json
    try:
        with open(Path_Dataset_Num, "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        eMessage = "Dataset Data could not be saved \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def readDatasetNum():
    """
    Datensatz Informationen werden aus einer json Datei gelesen und zurückgegeben
    """

    with open(Path_Dataset_Num, 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)
        for i in json_object['Datensatz']:
            date = i["Date"]
            num = i["Number"]
            images = i["Images"]

        return num, images, date

def addDatabaseDataset(value):
    """
    Setzt den übergebenen Wert in der mysql Tabelle
    """
    #print(text)
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="ailand",
          password="etarob",
          database="handwagen"
        )

        text = "INSERT INTO Datasets VALUES (\"" + value[0] + "\",\"" + value[2] + "\",\"" + value[3] + \
            "\",\"" + value[4] + "\",\"" + value[5] + "\",\"" + value[6] + "\",\"\",\"\",\"\");"

        mycursur = mydb.cursor()
        mycursur.execute(text)

        mydb.commit()
    except Exception as e:
        eMessage = "Saving Dataset to Database failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def changeDatabaseDataset(column, value, type, id):
    """
    Setzt den übergebenen Wert in der mysql Tabelle
    """
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="ailand",
          password="etarob",
          database="handwagen"
        )
        valueText = ""
        if type == "array":
            for i in value:
                valueText = valueText + i + " "
        else:
            valueText = value
        mycursur = mydb.cursor()
        mycursur.execute("UPDATE Datasets SET " + column + " = '" + valueText + "' WHERE Time = \"" + id + "\"")

        mydb.commit()
    except Exception as e:
        eMessage = "Changing Datasat Data in Database failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def deleteDatabaseDataset(id):
    """
    Setzt den übergebenen Wert in der mysql Tabelle
    """
    #print(text)
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="ailand",
          password="etarob",
          database="handwagen"
        )

        mycursur = mydb.cursor()
        mycursur.execute("DELETE  FROM Datasets WHERE Time = \"" + id + "\"")

        mydb.commit()
    except Exception as e:
        eMessage = "Deleting Dataset Data from Database failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def getcheckBox():
    """
    Checkbox für Tabelle wird erstellt und zurückgegeben
    """

    chkBoxSelection = QTableWidgetItem()
    chkBoxSelection.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
    chkBoxSelection.setCheckState(Qt.Unchecked)

    return chkBoxSelection

def deleteOldDatasets(data):

    num = 0
    maxNum = len(data) - 1
    while num <= maxNum:
        try:
            status = data[num][7]
            oldDate = data[num][0]
            #print("olddate: " + str(oldDate))
            dateArray = oldDate.split(".")
            newDate = ""
            for i in dateArray:
                newDate = newDate + i
            #print("newDate: " + newDate)
            #newDate = "Do Junu 1 12:43:12 2023"
            date = datetime.strptime(newDate, '%a %b %d %X %Y')
            time = datetime.now()
            #print("time: " + str(time))
            now = time - date
            #print("now: " + str(now))
            #print("date: " + str(oldDate) + "now: " + str(now))
            if now.days > 14:
                if status == "vollständig":
                    print("delete Dataset")
                    for n in data[num][9]:
                        imageName = Path_Image_Files + n + ".jpg"
                        fileName = Path_Image_Files + n + ".json"
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
                    deleteDatabaseDataset(oldDate)
                    data.pop(num)
                    num = num - 1
                    maxNum = maxNum - 1
        except Exception as e:
            eMessage = "Old Datasets could not be deleted \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
        num = num + 1
    #writeDatasetData(data)

def readDatasetData():
    """
    Datensatz Informationen werden aus einer json Datei gelesen und zurückgegeben
    """

    datasets = []

    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="ailand",
          password="etarob",
          database="handwagen"
        )

        mycursur = mydb.cursor()
        mycursur.execute("SELECT * FROM Datasets")

        myresult = mycursur.fetchall()
        mydb.commit()
        #print("Database: " + str(myresult))

        for x in myresult:
            #print("len: " + str(len(x)))
            text = str(x[7])
            imageNames = []
            iNames = text.split(" ")
            for j in iNames:
                if j != "":
                    imageNames.append(j)
            #print("imageNames: " + str(imageNames))
            text2 = str(x[8])
            uploadImages = []
            uNames = text2.split(" ")
            for y in uNames:
                if y != "":
                    uploadImages.append(y)
            #print("uploadImages: " + str(uploadImages))
            dataset = [ x[0], "", x[1], x[2], x[3], x[4], x[5], x[6], getcheckBox(), imageNames, uploadImages]
            #print("dataset:" + str(dataset))
            datasets.append(dataset)


    except Exception as e:
        eMessage = "Getting Database Data failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
    """
    with open('/home/ailand/GUI/Data/Datasets.json', 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)
        for i in json_object['Datensatz']:
            imageNames = []
            uploadImages = []
            for j in i["Images"]:
                imageNames.append(j)
            for k in i["UploadImages"]:
                uploadImages.append(k)
            lenNames = len(imageNames)
            lenUpload = len(uploadImages)
            if lenUpload == 0:
                uploadStatus = "vollständig"
            elif lenUpload < lenNames:
                uploadStatus = "unvollständig"
            else:
                uploadStatus = "fehlgeschlagen"

            dataset = [ i['Time'], i['Business'], i['Cultivation'], i['BBCH'], i['Light'], i['Ground'], i['ImageNum'], uploadStatus, getcheckBox(), imageNames, uploadImages]
            datasets.append(dataset)
    """
    return datasets

"""
def readData():
    with open("data.json", "r") as myfile:
        data=myfile.read()

    obj = json.loads(data)
    return obj
"""

def makeJsonData(data, time, imageData, server):
    """
    Übergebene Bild und Datensatz Informationen werden in eine json Datei geschrieben
    """
    usecaseIdQa = "fde742c8-51ab-4d8d-94ad-f3667bdb22cd"
    usecaseIdProd = "eb40faa4-45b5-4188-8fbc-70a4d1e39687"
    if server == "QA":
        cultivation = cultivationId[data[0]]
        id = codeId[data[0]]
        scopeValue = scopeId[data[0]]
        test_data = True
        usecaseId = usecaseIdQa
    else:
        cultivation = cultivationIdProd[data[0]]
        id = codeIdProd[data[0]]
        scopeValue = scopeIdProd[data[0]]
        test_data = False
        usecaseId = usecaseIdProd
    typeName1 = type1[data[0]]
    typeName2 = type2[data[0]]
    genotype = "genotype-" + data[9]
    light = "light_conditions-" + lightEn[data[1]]
    ground = "wetness-" + groundEn[data[3]]
    bbch = "bbch-" + data[2]
    imgDataText = imageData.split(";")
    if len(imgDataText) >= 3:
        exposureText = (imgDataText[0]).split("Exposure: ")
        if len(exposureText) >= 2:
            exposure = "EXIF_exposure-" + exposureText[1]
        else:
            print("No Camera Exposure Time Value found")
            exposure = "EXIF_exposure-None"
        gainText = (imgDataText[1]).split("Gain: ")
        if len(gainText) >= 2:
            gain = "EXIF_gain-" + gainText[1]
        else:
            print("No Camera Gain Value found")
            gain = "EXIF_gain-None"
        wbText = (imgDataText[2]).split(" WB:")
        if len(wbText) >= 2:
            wbText2 = (wbText[1]).split("'")
            wbValue = wbText2[0]
            wbValue = wbValue.split(" ")
            if len(wbValue) >= 4:
                wbValueR = "EXIF_white_balance_R-" + wbValue[1]
                wbValueG = "EXIF_white_balance_G-" + wbValue[2]
                wbValueB = "EXIF_white_balance_B-" + wbValue[3]
            else:
                print("No Camera WB Value found")
                wbValueR = "EXIF_white_balance_R-None"
                wbValueG = "EXIF_white_balance_G-None"
                wbValueB = "EXIF_white_balance_B-None"

        else:
            print("No Camera WB Value found")
            wbValueR = "EXIF_white_balance_R-None"
            wbValueG = "EXIF_white_balance_G-None"
            wbValueB = "EXIF_white_balance_B-None"
    else:
        print("No Camera Data Values found")
        exposure = "EXIF_exposure-None"
        gain = "EXIF_gain-NoneNone"
        wbValueR = "EXIF_white_balance_R-None"
        wbValueG = "EXIF_white_balance_G-None"
        wbValueB = "EXIF_white_balance_B-None"



    if data[4] == 0:
        influences = "comment_environment-None"
    else:
        influences = "comment_environment-" + Influences[data[4]]

    if data[5] == 0:
        infestation = "comment_weeds-None"
    else:
        infestation = "comment_weeds-" + Infestation[data[5]]

    if data[6] == "":
        distance = "distance-0"
    else:
        distance = "distance-" + data[6]
    """
    if data[7] == 0:
        #lon = 0
    else:
        lon = data[7]

    if data[8] == 0:
        lat = 0
    else:
        lat = data[8]
    """

    imgData = {
    "images": [
      {
        "sequence_id": 0,
        "test_data": test_data,
        "app": {
          "name": "FieldCatcherEye",
          "version": "0.0.1"
        },
        "legal": {
          "source": "FieldCatcherEye",
          "restricted_share": False,
          "restricted_use": False
        },
        "camera": {
          "manufacturer": "Daheng",
          "name": "MER2-630-60U3C",
          "software": "0.0.1"
        },
        "image": {
          "country_code": "DE",
          "capture": time,
          "location": {
            "lon": data[7],
            "lat": data[8]
          },
          "altitude": 0
        },
        "custom_data": [
          {
            "key": "genotype",
            "value": genotype,
            "type": "STRING"
          },
          {
            "key": "light_conditions",
            "value": light,
            "type": "STRING"
          },
          {
            "key": "bbch",
            "value": bbch,
            "type": "STRING"
          },
          {
            "key": "wetness",
            "value": ground,
            "type": "STRING"
          },
          {
            "key": "distance",
            "value": distance,
            "type": "STRING"
          },
          {
            "key": "comment_environment",
            "value": influences,
            "type": "STRING"
          },
          {
            "key": "comment_weeds",
            "value": infestation,
            "type": "STRING"
          },
          {
            "key": "device_number",
            "value": data[11],
            "type": "STRING"
          },
          {
            "key": "sensorbox_number",
            "value": data[10],
            "type": "STRING"
          },
          {
            "key": "EXIF_gain",
            "value": gain,
            "type": "STRING"
          },
          {
            "key": "EXIF_exposure",
            "value": exposure,
            "type": "STRING"
          },
          {
            "key": "EXIF_white_balance_R",
            "value": wbValueR,
            "type": "STRING"
          },
          {
            "key": "EXIF_white_balance_G",
            "value": wbValueG,
            "type": "STRING"
          },
          {
            "key": "EXIF_white_balance_B",
            "value": wbValueB,
            "type": "STRING"
          },
          {
            "key": "matching_id",
            "value": "matching_id-None",
            "type": "STRING"
          }
        ],
        "content": {
          "user_sources": [
            {
              "sequence_id": 0,
              "user_id": "214f4eca-cf99-4756-a420-935912b9c608",
              "tool_id": "ff4c2aa4-225c-42e3-9614-44f4e038f310"
            }
          ],
          "usecases": [
            {
              "sequence_id": 0,
              "label": usecaseId,
              "status": "initial",
              "annotations": [
                {
                  "sequence_id": 0,
                  "source_type": "user",
                  "ref_source_sequence_id": 0,
                  "tags": [
                    {
                      "type": "scope",
                      "value": "3a381026-d31d-4db5-9e96-aa6ed40b727a"
                    },
                    {
                      "type": "usecase",
                      "value": usecaseId
                    }
                  ]
                },
                {
                  "sequence_id": 1,
                  "source_type": "user",
                  "ref_source_sequence_id": 0,
                  "tags": [
                    {
                      "type": "scope",
                      "value": scopeValue
                    },
                    {
                      "type": typeName1,
                      "value": id
                    },
                    {
                      "type": typeName2,
                      "value": cultivation
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    ]
  }

    #writeData(imgData, imgNames)
    return imgData


def setData(table, data):
    """
    Übergebene Daten werden der Tabelle hinzugefügt
    """

    n = 0
    k = 0
    #while k < 10:
        #table.insertRow(k);
        #k = k +1

    if len(data) > 0:
        for i in data:

            addData(table, data[n], n)
            n = n + 1

def addData(table, data, row):
    """
    Neue Tabellen Zeile wird erstellt und die übergebenen Daten eingetragen
    """

    table.insertRow(0);

    itemDate = QTableWidgetItem()
    itemDate.setText(str(data[0]))
    itemDate.setTextAlignment(Qt.AlignCenter)
    table.setItem(0,0,itemDate)

    #itemBusiness = QTableWidgetItem()
    #itemBusiness.setText(str(data[1]))
    #table.setItem(0,1,itemBusiness)

    itemCultivation = QTableWidgetItem()
    itemCultivation.setText(str(data[2]))
    itemCultivation.setTextAlignment(Qt.AlignCenter)
    table.setItem(0,1,itemCultivation)

    itemBBCH = QTableWidgetItem()
    itemBBCH.setText(str(data[3]))
    itemBBCH.setTextAlignment(Qt.AlignCenter)
    table.setItem(0,2,itemBBCH)

    itemLight = QTableWidgetItem()
    itemLight.setText(str(data[4]))
    itemLight.setTextAlignment(Qt.AlignCenter)
    table.setItem(0,3,itemLight)

    itemGround = QTableWidgetItem()
    itemGround.setText(str(data[5]))
    itemGround.setTextAlignment(Qt.AlignCenter)
    table.setItem(0,4,itemGround)

    itemImageNum = QTableWidgetItem()
    itemImageNum.setText(str(data[6]))
    itemImageNum.setTextAlignment(Qt.AlignCenter)
    table.setItem(0,5,itemImageNum)

    itemResponse = QTableWidgetItem()
    itemResponse.setText(str(data[7]))
    if data[7] != "":
        itemResponse.setBackground(getTableItemColor(data[7]))
    table.setItem(0,6,itemResponse)

    table.setItem(0,7,data[8])

def updateTable(table, col, data, datasets):
    try:
        datasetNum = len(datasets) - 1

        colText = ""

        if col == 0:
            datasetCol = col
        else:
            datasetCol = col + 1

        if col == 1:
            colText = "Cultivation"
        elif col == 2:
            colText = "BBCH"
        elif col == 3:
            colText = "Light"
        elif col == 4:
            colText = "Ground"


        table.item(0,col).setText(data)
        datasets[datasetNum][datasetCol] = data
        id = datasets[datasetNum][0]
        if colText != "":
            changeDatabaseDataset(colText, data, "text", id)
        #writeDatasetData(datasets)
    except Exception as e:
        eMessage = "Updating Table failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)


def getTableItemColor(text):
    """
    Farbe zum übergebenen response wird zurückgegeben
    """
    color = ""

    if text == "fehlgeschlagen":
        color = QColor(255,0,0)
    if text == "unvollständig":
        color = QColor(255,255,0)
    if text == "vollständig":
        color = QColor(0,255,0)

    return color


def getGPSData():
    """
    GPS Daten werden ermittelt und zurückgegeben
    """
    lng = "0"
    lat = "0"
    out = ""
    try:
        gpsSettings = Path_GPS_Settings
        gpsCommand = Path_GPS_Command
        procSettings = subprocess.Popen([gpsSettings], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        proc = subprocess.Popen([gpsCommand], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        (out, err) = proc.communicate()
    except Exception as e:
        eMessage = "GPS File could not be executed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

    textOut = str(out)
    #print(textOut)
    text = textOut.split("longitude:")
    if len(text) >= 2:
        longitude = text[1].split("latitude:")
        longitudeNum = longitude[0].split("\\")
        lng = longitudeNum[0]
        lng2 = lng.split(",")
        if len(lng2) >= 2:
            lng = lng2[0] + "." + lng2[1]
        print("longitude:" + lng)
        if len(longitude) >= 2:
            latitude = longitude[1].split("altitude:")
            latitudeNum = latitude[0].split("\\")
            lat = latitudeNum[0]
            lat2 = lat.split(",")
            if len(lat2) >= 2:
                lat = lat2[0] + "." + lat2[1]
            print("latitude:" + lat)
        else:
            print("No latitude Found")

    else:
        print("No longitude Found")
    
    return float(lng), float(lat)




def dataUpload(dataNames, datasets, table, row, labelUpload, buttonUpload, selected, incomplete, server):
    """
    Übergebene Bildere und Json Dateien werden hochgeladen und eine Rückmeldung zurückgegeben
    """
    #while uploadStatus:
        #time.sleep(1)
        #print(uploadStatus)
    #uploadStatus = True
    output = ""
    out = ""
    numSucess = 0
    numError = 0
    result = ""
    failedImages = []
    uploadText = labelUpload.text()
    uploadNum = 0
    uploadMaxNum = len(dataNames)
    labelUpload.setText(uploadText + " " + str(uploadNum) + "/" + str(uploadMaxNum))
    #print("server: " + server)
    if server == "QA":
        uploadFile = "ingestionQa.sh "
    else:
        uploadFile = "ingestionProd.sh "
    #print(uploadFile)
    for i in dataNames:
        imageResult = "fehlgeschlagen"
        textUpload = Path_Upload_Skript + uploadFile + i
        try:
            proc = subprocess.Popen([textUpload], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            (out, err) = proc.communicate()
        except Exception as e:
            eMessage = "Upload File could not be executed \n" + str(e)
            print(eMessage)
            writeLog("Error", eMessage)
        textOut = str(out)
        text = textOut.split("HTTP")
        if len(text) >= 4:
            httpText = text[3].split(" ")
            if len(httpText) >= 2:
                result = httpText[1]
                if result == "200":
                    numSucess = numSucess + 1
                    imageResult = "erfolgreich"
                else:
                    numError = numError + 1
                    failedImages.append(i)
            else:
                numError = numError + 1
                failedImages.append(i)
        else:
            numError = numError + 1
            failedImages.append(i)
        output = output + str(out) + "\n" + result + "\n"
        uploadNum = uploadNum + 1
        labelUpload.setText(uploadText + " " + str(uploadNum) + "/" + str(uploadMaxNum))
        #uploadWindow.addText("Bild hochladen: " + imageResult + " " + str(uploadNum) + "/" + str(uploadMaxNum))
        print("Bild hochladen: " + imageResult + " " + str(uploadNum) + "/" + str(uploadMaxNum))
        #print("NumS:" + str(numSucess))
        #print("NumE:" + str(numError))
    if numSucess == 0:
        #print("Num:" + str(numError))
        #print("Upload Failed")
        if incomplete:
            result = "unvollständig"
            color = getTableItemColor("unvollständig")
        else:
            result = "fehlgeschlagen"
            color = getTableItemColor("fehlgeschlagen")
    elif numSucess != 0 and numError != 0:
        #print("Upload Sucess Partly")
        result = "unvollständig"
        color = getTableItemColor("unvollständig")
    elif numSucess != 0 and numError == 0:
        #print("Upload Sucess")
        result = "vollständig"
        color = getTableItemColor("vollständig")
    #print(str(out))
    datasetNum = len(datasets) - (1 + row)
    datasets[datasetNum][7] = result
    datasets[datasetNum][10] = failedImages
    table.item(row,6).setText(result)
    table.item(row,6).setBackground(color)
    labelUpload.hide()
    id = datasets[datasetNum][0]
    changeDatabaseDataset("Upload", result, "text", id)
    changeDatabaseDataset("UploadImages", failedImages, "array", id)
    #uploadWindow.addText("Upload Dataset finished Result: " + result)
    print("Upload Dataset finished Result: " + result)
    #writeDatasetData(datasets)
    labelUpload.setText(uploadText)
    logText = "Dataset: " + str(datasets[datasetNum][0]) + " Result: " + result
    writeLog("upload", logText)
    if selected == False:
        buttonUpload.setEnabled(True)
        #buttonUpload.setStyleSheet("background-color: green; height: 100")
    #uploadStatus = False
    #print(output)
    return result


