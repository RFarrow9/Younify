from younify import yt_frontend, framework
import unittest
import qdarkstyle


class TestFrameworkMethods(unittest.TestCase):
    def setup_empty(self):
        self.WorkingURLs = framework.working()
        self.FailedURLs = framework.failed()
        self.ProcessedURLs = framework.processed()
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()

    def test_launch_gui(self):
        self.setup_empty()
        app = yt_frontend.QApplication(["Younify"])
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        app.setWindowIcon(yt_frontend.QtGui.QIcon(yt_frontend.icon))
        self.WorkingURLs.add_url("YSkIJTIE45c")
        self.WorkingURLs.add_url("B2KAipyP8mc")
        myWindow = yt_frontend.MainWindow()
        myWindow.show()
        app.exec_()



if __name__ == '__main__':
    unittest.main()
