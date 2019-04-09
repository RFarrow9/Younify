#import time
from younify import yt_frontend
from younify import youtube_converter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
import json
from younify import breeze_resources
import ctypes
import unittest

class TestFrameworkMethods(unittest.TestCase):
    def launch_gui(self):
        app = QApplication(["Younify"])
        # trayIcon = QtWidgets.QWinTaskbarButton(QtGui.QIcon(icon), app)
        # trayIcon.show()
        file = QFile(":/dark.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        """Fix the dark theme, this may need recompiling from source"""
        # app.setStyleSheet(stream.readAll())
        app.setWindowIcon(QtGui.QIcon(icon))
        myWindow = MainWindow()
        myWindow.show()
        app.exec_()

if __name__ == '__main__':
    unittest.main()
