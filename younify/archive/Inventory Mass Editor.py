import datetime
import random
import InventoryWrapper.Versions.Version0_0_0.ivm_wrapper as ivm_wrapper
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class DataBase:
    session = ""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.start_screen = SessionConfig()
        self.type_picker = TypePicker()
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.type_picker)
        self.central_widget.setCurrentWidget(self.start_screen)

        self.start_screen.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.type_picker))
        self.type_picker.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))


class SessionConfig(QWidget):

    clicked = pyqtSignal()

    def __init__(self):
        super(SessionConfig, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Server (eg. https://server.company.com:8483"))
        self.server_field = QLineEdit("https://10.134.66.112:8483")
        self.layout.addWidget(self.server_field)

        self.layout.addWidget(QLabel("Username"))
        self.username_field = QLineEdit("mkennedy")
        self.layout.addWidget(self.username_field)

        self.layout.addWidget(QLabel("Password"))
        self.password_field = QLineEdit("password")
        self.password_field.setEchoMode(2)
        self.layout.addWidget(self.password_field)

        auth_button = QPushButton("Authenticate")
        self.layout.addWidget(auth_button)
        auth_button.clicked.connect(self.test_auth)

        self.setLayout(self.layout)

    def test_auth(self):
        DataBase.session = ivm_wrapper.IvmSession(self.server_field.text(),
                                                  self.username_field.text(),
                                                  self.password_field.text())
        if DataBase.session.token is None:
            failure = QLabel("That did not work.")
            self.layout.addWidget(failure)
            self.setLayout(self.layout)
        else:
            success = QLabel("Success!")
            self.layout.addWidget(success)

            switch_button = QPushButton("Switch")
            self.layout.addWidget(switch_button)
            switch_button.clicked.connect(self.clicked.emit)

            self.setLayout(self.layout)


class TypePicker(QWidget):

    clicked = pyqtSignal()

    def __init__(self):
        super(TypePicker, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        self.checks = []
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Enter your desired domain below:"))

        self.domain_field = QLineEdit("equipment")
        self.layout.addWidget(self.domain_field)

        types_button = QPushButton("Get Types")
        self.layout.addWidget(types_button)

        self.update_button = QPushButton("Update Types")
        self.update_button.clicked.connect(self.print_selected)

        types_button.clicked.connect(self.get_types)

        self.setLayout(self.layout)

        self.all_check = QCheckBox("All - Check to select all; uncheck to clear all.")
        self.all_check.stateChanged.connect(self.set_all)

    def get_types(self):
        types_array = DataBase.session.get_types(self.domain_field.text())
        types_config = ivm_wrapper.IvmTypeConfig(self.domain_field.text(), types_array)
        type_names = types_config.type_names()

        result_layout = self.layout

        result_layout.addWidget(self.update_button)
        result_layout.addWidget(self.all_check)

        if len(self.checks) != 0:
            for c in self.checks:
                c.hide()

        self.checks = []
        for x in type_names:
            c = QCheckBox(x)
            result_layout.addWidget(c)
            self.checks.append(c)

        self.setLayout(result_layout)

    def set_all(self):
        if self.all_check.checkState():
            for x in self.checks:
                x.setChecked(True)
        else:
            for x in self.checks:
                x.setChecked(False)

    def print_selected(self):
        result_array = []
        for x in self.checks:
            if x.checkState():
                result_array.append(x.text())
        update_dates(DataBase.session, result_array)


def random_future_date():
    today = datetime.datetime.today()
    new_date = today + datetime.timedelta(days=random.randint(10, 41))
    new_date = new_date.strftime("%Y-%m-%d")
    return new_date


def update_dates(session, types):
    for x in types:
        search = session.search_items("equipment", x)
        items = search["items"]

        print(x + ": " + str(len(items)))

        for item in items:
            if item.type.lower().replace(" ", "") == x.lower().replace(" ", ""):
                item.edit_attribute("core/lastEventDate", str(random_future_date()))
                item.edit_attribute("core/lastEvent", "Calibration")
                session.save_item(item)
            else:
                pass


app = QApplication([])
myWindow = MainWindow()
myWindow.show()
app.exec_()
