# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class UploadWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0,0, 600, 600)

        self.textFont = QFont()
        self.textFont.setPointSize(15)
        #self.textFont.setBold(True)
        self.text = ""

        layout = QVBoxLayout()
        self.label = QLabel("")
        #self.label.setStyleSheet("background-color: yellow; color: black")
        self.label.setFont(self.textFont)
        self.textArea = QPlainTextEdit(self)
        self.textArea.resize(400, 200)
        layout.addWidget(self.textArea)
        self.setLayout(layout)

    def addText(self, msg):
        print("test")
        self.text = self.text + "\n" + msg
        self.textArea.setPlainText(self.text)
        #self.label.setText(self.text)

    def cleanWindow(self):
        self.label.setText("")
        self.text = ""
