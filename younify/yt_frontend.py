from younify import youtube_converter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import json
import breeze_resources

with open('c:\\config\\config.json') as f:
    config = json.load(f)

icon = config["yt_frontend"]["icon"]

def main():
    app = QApplication(["Younify"])
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    app.setWindowIcon(QtGui.QIcon(icon))
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle("Younify")
        self.central_widget = QStackedWidget()
        self.table_widget = MyTableWidget(self)

        #self.setCentralWidget(self.central_widget)
        self.setCentralWidget(self.table_widget)

        self.start_screen = StartWindow()
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.setCurrentWidget(self.start_screen)

class StartWindow(QWidget):
    def __init__(self):
        super(StartWindow, self).__init__()
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

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        @pyqtSlot()
        def on_click(self):
            print("\n")
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    main()
