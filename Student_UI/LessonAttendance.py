import sys, os
sys.path.append(os.getcwd())

from Classes.user import User
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import *
from pathlib import Path


class LessonAttendance(QMainWindow):
    def __init__(self, email):
        super().__init__()
        self.email = email
        self.setWindowTitle("Lesson Attendance Window")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        self.show_Lesson_Attendance()

        self.setMinimumSize(500, 500)

    def show_Lesson_Attendance(self):
        table_lesson = User.get_Lesson_Attendance_Student(self.email)
        layout = QVBoxLayout()
        layout.addWidget(table_lesson)
        self.table_view.setLayout(layout)


def lesson_attendance():
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("lightstyle.qss").read_text())
    window = LessonAttendance()
    window.setStyleSheet(Path("lightstyle.qss").read_text())
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    lesson_attendance()
