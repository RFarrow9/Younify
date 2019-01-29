import youtube_converter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.start_screen = StartWindow()
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.setCurrentWidget(self.start_screen)


class StartWindow(QWidget):
    def __init__(self):
       #super(SessionConfig, self).__init__()
        QWidget.__init__(self)
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Enter the URL you Son of a Bitch:"))
        self.server_field = QLineEdit("")
        self.layout.addWidget(self.url_field)

        self.layout.addWidget(QLabel("Enter the artist you Son of a Bitch"))
        self.password_field = QLineEdit("")
        self.layout.addWidget(self.artist_field)

        self.layout.addWidget(QLabel("Enter the song title you... nah you're alright"))
        self.username_field = QLineEdit("")
        self.layout.addWidget(self.title_field)

        button = QPushButton("Do the thing... YOU SON OF A BITCH")
        self.layout.addWidget(button)
        button.clicked.connect()
        button.clicked.connect(lambda: youtube_converter.get_audio(self.url_field.text, self.artist_field.text, self.title_field.text))

        self.setLayout(self.layout)


app = QApplication([])
myWindow = MainWindow()
myWindow.show()
app.exec_()
