from younify import youtube_converter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
import json
from younify import breeze_resources
import ctypes

with open('c:\\config\\config.json') as f:
    config = json.load(f)

icon = config["yt_frontend"]["icon"]
myappid = "rftech.younify.1.1"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def main():
    app = QApplication(["Younify"])
    #trayIcon = QtWidgets.QWinTaskbarButton(QtGui.QIcon(icon), app)
    #trayIcon.show()
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    """Fix the dark theme, this may need recompiling from source"""
    #app.setStyleSheet(stream.readAll())
    app.setWindowIcon(QtGui.QIcon(icon))
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 500, 200)
        self.setWindowTitle("Younify")
        self.central_widget = QStackedWidget()
        self.table_widget = TabTable(self)
        self.setCentralWidget(self.table_widget)


class TabTable(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.manual_screen = ManualWindow()
        self.yt_settings_screen = YTSettingsWindow()
        self.sp_settings_screen = SPSettingsWindow()
        self.advanced_settings_screen = AdvancedSettingsWindow()
        self.processing_screen = ProcessingWindow()
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        # Add tabs
        self.tabs.addTab(self.tab1, "Manual Run")
        self.tabs.addTab(self.tab2, "Youtube Settings")
        self.tabs.addTab(self.tab3, "Spotify Settings")
        self.tabs.addTab(self.tab4, "Advanced Settings")
        self.tabs.addTab(self.tab5, "Processing")
        # Create first tab
        self.tab1.layout = QVBoxLayout(self.tab1)
        self.tab2.layout = QVBoxLayout(self.tab2)
        self.tab3.layout = QVBoxLayout(self.tab3)
        self.tab4.layout = QVBoxLayout(self.tab4)
        self.tab5.layout = QVBoxLayout(self.tab5)
        self.tab1.layout.addWidget(self.manual_screen)
        self.tab2.layout.addWidget(self.yt_settings_screen)
        self.tab3.layout.addWidget(self.sp_settings_screen)
        self.tab4.layout.addWidget(self.advanced_settings_screen)
        self.tab5.layout.addWidget(self.processing_screen)
        #self.central_widget.addWidget(self.start_screen)
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        self.tab3.setLayout(self.tab3.layout)
        self.tab4.setLayout(self.tab4.layout)
        self.tab5.setLayout(self.tab5.layout)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        @pyqtSlot()
        def on_click(self):
            print("\n")
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class ManualWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self.inner_layout1 = QHBoxLayout()
        self.inner_layout2 = QHBoxLayout()
        self.inner_layout3 = QHBoxLayout()
        self.url_field = QLineEdit()
        self.artist_field = QLineEdit()
        self.title_field = QLineEdit()

        self.url_field.setPlaceholderText("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.artist_field.setPlaceholderText("The Beegees")
        self.title_field.setPlaceholderText("Stayin' Alive")

        self.inner_layout1.addWidget(CustomQLabel("Youtube URL:",))
        self.inner_layout1.addWidget(self.url_field)

        self.inner_layout2.addWidget(CustomQLabel("Artist: "))
        self.inner_layout2.addWidget(self.artist_field)

        self.inner_layout3.addWidget(CustomQLabel("Song title:"))
        self.inner_layout3.addWidget(self.title_field)

        self.layout.addLayout(self.inner_layout1)
        self.layout.addLayout(self.inner_layout2)
        self.layout.addLayout(self.inner_layout3)
        button = QPushButton("Process URL")
        self.layout.addWidget(button)
        #button.clicked.connect(lambda: youtube_converter._process_url([self.url_field.text()],
        #                                                              self.artist_field.text(),
        #                                                              self.title_field.text()))
        self.setLayout(self.layout)

class CustomQLineEdit(QLineEdit):
    def __init__(self, text="Don't mind me."):
        """"Looks like the super call is showing the Qline behind by default"""
        super().__init__()
        self.textEditor=QLineEdit(self)
        self.textEditor.setPlaceholderText(text)
        self.textEditor.show()
        #self.setGeometry(0, 0, 2000, 50)

class CustomQLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.setMinimumWidth(130)
        self.setText(text)
        self.show()

class YTSettingsWindow(QWidget):
    def __init__(self):
        super(YTSettingsWindow, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        #Method to put in a default value if this is empty,
        # can use the QLineEdit.selectionChanged method and check for empty string literals
        self.layout.addWidget(QLabel("Enter the URL"))
        self.url_field = QLineEdit("")
        self.layout.addWidget(self.url_field)
        self.layout.addWidget(QLabel("Enter the artist "))
        self.artist_field = QLineEdit("")
        self.layout.addWidget(self.artist_field)
        self.layout.addWidget(QLabel("Enter the song title"))
        self.title_field = QLineEdit("")
        self.layout.addWidget(self.title_field)
        button = QPushButton("Do the thing")
        self.layout.addWidget(button)
        button.clicked.connect(lambda: youtube_converter.Url([self.url_field.text()],
                                                             self.artist_field.text(),
                                                             self.title_field.text()))
        self.setLayout(self.layout)

class SPSettingsWindow(QWidget):
    def __init__(self):
        super(SPSettingsWindow, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Enter the URL"))
        self.url_field = QLineEdit("")
        self.layout.addWidget(self.url_field)
        self.layout.addWidget(QLabel("Enter the artist "))
        self.artist_field = QLineEdit("")
        self.layout.addWidget(self.artist_field)
        self.layout.addWidget(QLabel("Enter the song title"))
        self.title_field = QLineEdit("")
        self.layout.addWidget(self.title_field)
        button = QPushButton("Do the thing")
        self.layout.addWidget(button)
        button.clicked.connect(lambda: youtube_converter.Url([self.url_field.text()],
                                                             self.artist_field.text(),
                                                             self.title_field.text()))
        self.setLayout(self.layout)

class AdvancedSettingsWindow(QWidget):
    def __init__(self):
        super(AdvancedSettingsWindow, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Enter the URL"))
        self.url_field = QLineEdit("")
        self.layout.addWidget(self.url_field)
        self.layout.addWidget(QLabel("Enter the artist "))
        self.artist_field = QLineEdit("")
        self.layout.addWidget(self.artist_field)
        self.layout.addWidget(QLabel("Enter the song title"))
        self.title_field = QLineEdit("")
        self.layout.addWidget(self.title_field)
        button = QPushButton("Do the thing")
        self.layout.addWidget(button)
        button.clicked.connect(lambda: youtube_converter.Url([self.url_field.text()],
                                                             self.artist_field.text(),
                                                             self.title_field.text()))
        self.setLayout(self.layout)

class ProcessingWindow(QWidget):
    def __init__(self):
        super(ProcessingWindow, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Enter the URL"))
        self.url_field = QLineEdit("")
        self.layout.addWidget(self.url_field)
        self.layout.addWidget(QLabel("Enter the artist "))
        self.artist_field = QLineEdit("")
        self.layout.addWidget(self.artist_field)
        self.layout.addWidget(QLabel("Enter the song title"))
        self.title_field = QLineEdit("")
        self.layout.addWidget(self.title_field)
        button = QPushButton("Do the thing")
        self.layout.addWidget(button)
        button.clicked.connect(lambda: youtube_converter.Url([self.url_field.text()],
                                                             self.artist_field.text(),
                                                             self.title_field.text()))
        self.setLayout(self.layout)

if __name__ == "__main__":
    print("nothing to do here")
