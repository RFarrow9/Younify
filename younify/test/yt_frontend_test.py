from younify import yt_frontend
import unittest

class TestFrameworkMethods(unittest.TestCase):
    def test_launch_gui(self):
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
