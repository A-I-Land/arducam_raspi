from log import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import mysql.connector


def addDatabaseImage(name):
    """
    Setzt eine neue Zeile für das übergebene Bild in der mysql Tabelle
    """
    #print(text)
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="ailand",
          password="etarob",
          database="handwagen"
        )

        text = "INSERT INTO Images VALUES (\"" + name + "\",\"notUploaded\",\"\");"

        #print(text)


        mycursur = mydb.cursor()
        mycursur.execute(text)

        mydb.commit()
    except Exception as e:
        eMessage = "Saving Image to Database failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def changeDatabaseImageValue(column, name, value):
    """
    Setzt den übergebenen Wert in der mysql Tabelle (Images)
    """
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="ailand",
          password="etarob",
          database="handwagen"
        )
        
        mycursur = mydb.cursor()
        mycursur.execute("UPDATE Images SET  " + column + " " + " = '" + value + "' WHERE Name = \"" + name + "\"")

        mydb.commit()
    except Exception as e:
        eMessage = "Changing Datasat Data in Database failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def readDatabaseImageStatus(name):
    """
    Image Status zum übergebenen Image wird gelesen und zurückgegeben
    """

    datasets = []
    result = ""

    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="ailand",
          password="etarob",
          database="handwagen"
        )

        mycursur = mydb.cursor()
        mycursur.execute("SELECT Status FROM Images WHERE Name=\"" + name + "\";")

        myresult = mycursur.fetchall()
        mydb.commit()

        #print(myresult)
        #print(myresult[0])

        text = str(myresult[0]).split("'")

        if len(text) >= 2:
            result = text[1]

        #print(result)
        return result
        


    except Exception as e:
        eMessage = "Reading Image Status from Database failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def deleteDatabaseDataset(id):
    """
    Löscht den übergebenen Datensatz in der mysql Tabelle
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



def addDatabaseDataset(value):
    """
    Setzt den übergebenen Datensatz in der mysql Tabelle
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

        #print(text)
        mycursur = mydb.cursor()
        mycursur.execute(text)

        mydb.commit()
    except Exception as e:
        eMessage = "Saving Dataset to Database failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)


def readDatasetData():
    """
    Datensatz Informationen werden aus der Datenbank gelesen und zurückgegeben
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

            chkBoxSelection = QTableWidgetItem()
            chkBoxSelection.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxSelection.setCheckState(Qt.Unchecked)

            dataset = [ x[0], "", x[1], x[2], x[3], x[4], x[5], x[6], chkBoxSelection, imageNames, uploadImages]
            #print("dataset:" + str(dataset))
            datasets.append(dataset)


    except Exception as e:
        eMessage = "Getting Database Data failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
    
    return datasets

def setDatabaseData(table, setting, value):
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

        mycursur = mydb.cursor()
        mycursur.execute("UPDATE " + table + " SET " + setting + " = '" + value + "' WHERE 1")

        mydb.commit()
    except Exception as e:
        eMessage = "Saving Data to Database failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)

def getDatabaseData(table, setting):
    """
    Gibt die Informationen der übergebenen mysql Tabelle zurück
    """
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="ailand",
          password="etarob",
          database="handwagen"
        )

        mycursur = mydb.cursor()
        mycursur.execute("SELECT " + setting + " FROM " + table)

        myresult = mycursur.fetchall()
        mydb.commit()
        for x in myresult:
            text = str(x)
            result = text.split(",")
            result = result[0].split("(")
        value = result[1]
    except Exception as e:
        eMessage = "Getting Database Data failed \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
        value = ""

    return value



