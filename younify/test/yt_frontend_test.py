from younify import yt_frontend
import unittest
import qdarkstyle


class TestFrameworkMethods(unittest.TestCase):
    def test_launch_gui(self):
        app = yt_frontend.QApplication(["Younify"])
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        app.setWindowIcon(yt_frontend.QtGui.QIcon(yt_frontend.icon))
        myWindow = yt_frontend.MainWindow()
        myWindow.show()
        app.exec_()


if __name__ == '__main__':
    unittest.main()
