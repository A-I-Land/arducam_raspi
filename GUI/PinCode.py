# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QLineEdit
from log import *
import os
import hashlib

Path_Password = "/home/ailand/GUI_Data/Data/pw.txt"


def setPinNumber(textfield, number):
    """
    Übergebene Nummer wird im Textfeld angezeigt
    """
    pincode = textfield.text() + number
    textfield.setText(pincode)

def deletePinNumber(textfield):
    """
    Letzte Nummer wird aus dem Textfeld entfernt
    """
    pincode = textfield.text()[:-1]
    textfield.setText(pincode)

def deleteText(textfield):
    """
    Kompletter Text wird aus dem Textfeld entfernt
    """
    textfield.setText("")

def readPinCode():
    """
    Key und Salt für den PinCode werden der Datei entnommen und zurückgegeben
    """
    with open(Path_Password, "rb") as myfile:
        storage=myfile.read()

    salt = storage[:32] # 32 is the length of the salt
    key = storage[32:]

    return key, salt

def encryptPin(pin, salt):
    """
    Pin wird verschlüsselt und der resultierende key zurückgegeben
    """

    newPin = str(pin)

    key = hashlib.pbkdf2_hmac(
        'sha256',
        newPin.encode('utf-8'), # Convert the password to bytes
        salt,
        100000
    )

    return key

def writeNewKey(key, salt):
    """
    Neuer Key wird zusammen mit dem Salt in eine Datei geschrieben
    """
    try:
        storage = salt + key
        with open(Path_Password, "wb") as outfile:
            outfile.write(storage)
    except Exception as e:
        eMessage = "New Key could not be saved \n" + str(e)
        print(eMessage)
        writeLog("Error", eMessage)
