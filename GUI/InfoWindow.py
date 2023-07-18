# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.textFont = QFont()
        self.textFont.setPointSize(20)
        self.textFont.setBold(True)

        layout = QVBoxLayout()
        self.label = QLabel("Achtung! Bilder sind eventuell unscharf bitte \n Bilder und Kamera überprüfen!!!")
        self.label.setStyleSheet("background-color: yellow; color: black")
        self.label.setFont(self.textFont)
        layout.addWidget(self.label)
        self.setLayout(layout)
