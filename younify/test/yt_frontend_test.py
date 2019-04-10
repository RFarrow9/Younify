from younify import yt_frontend
import unittest

class TestFrameworkMethods(unittest.TestCase):
    def test_launch_gui(self):
        app = yt_frontend.QApplication(["Younify"])
        # trayIcon = QtWidgets.QWinTaskbarButton(QtGui.QIcon(icon), app)
        # trayIcon.show()
        file = yt_frontend.QFile(":/dark.qss")
        file.open(yt_frontend.QFile.ReadOnly | yt_frontend.QFile.Text)
        stream = yt_frontend.QTextStream(file)
        """Fix the dark theme, this may need recompiling from source"""
        # app.setStyleSheet(stream.readAll())
        app.setWindowIcon(yt_frontend.QtGui.QIcon(yt_frontend.icon))
        myWindow = yt_frontend.MainWindow()
        myWindow.show()
        app.exec_()

if __name__ == '__main__':
    unittest.main()
