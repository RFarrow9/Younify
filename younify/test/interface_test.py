from younify import interface, frames, motley
import unittest, logging
import qdarkstyle

motley.setup_logger(__name__)
log = logging.getLogger(__name__)


class TestFrameworkMethods(unittest.TestCase):
    def setup_empty(self):
        self.WorkingURLs = frames.working
        self.FailedURLs = frames.failed
        self.ProcessedURLs = frames.processed
        self.WorkingURLs.truncate_urls()
        self.ProcessedURLs.truncate_urls()
        self.FailedURLs.truncate_urls()

    def test_launch_gui(self):
        self.setup_empty()
        app = interface.QApplication(["Younify"])
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        app.setWindowIcon(interface.QtGui.QIcon(interface.icon))
       # self.WorkingURLs.push_url_to_queue("YSkIJTIE45c")
       # self.WorkingURLs.push_url_to_queue("B2KAipyP8mc")
       # self.WorkingURLs.push_url_to_queue("W2IIfWveZSg")
        myWindow = interface.MainWindow()
        myWindow.show()
        app.exec_()


if __name__ == '__main__':
    unittest.main()
