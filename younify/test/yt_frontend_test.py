from younify import yt_frontend, framework
import unittest
import qdarkstyle

class TestFrameworkMethods(unittest.TestCase):
    def setup_empty(self):
        self.WorkingURLs = framework.working
        self.FailedURLs = framework.failed
        self.ProcessedURLs = framework.processed
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()

    def test_launch_gui(self):
        self.setup_empty()
        app = yt_frontend.QApplication(["Younify"])
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        app.setWindowIcon(yt_frontend.QtGui.QIcon(yt_frontend.icon))
       # self.WorkingURLs.push_url_to_queue("YSkIJTIE45c")
       # self.WorkingURLs.push_url_to_queue("B2KAipyP8mc")
       # self.WorkingURLs.push_url_to_queue("W2IIfWveZSg")
        myWindow = yt_frontend.MainWindow()
        myWindow.show()
        app.exec_()


if __name__ == '__main__':
    unittest.main()
