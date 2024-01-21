import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_main_3 import Ui_MainWindow
from pathlib import Path

class loginWindow(QMainWindow):
    def __init__(self):
        super(loginWindow, self).__init__()
        self.loginWindow.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_window = loginWindow()
    app_window.setStyleSheet(Path("lightstyle.qss").read_text())
    app_window.show()
    sys.exit(app.exec_())
