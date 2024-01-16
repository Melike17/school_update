import sys, os
sys.path.append(os.getcwd())

from Classes.user import User
from PyQt5.QtWidgets import *

class LessonAttendance(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lesson Attendance Window")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        self.show_Lesson_Attendance()

    def show_Lesson_Attendance(self):
        table_lesson = User.get_Lesson_Attendance()
        layout = QVBoxLayout()
        layout.addWidget(table_lesson)
        self.table_view.setLayout(layout)


def lesson_attendance():
    app = QApplication(sys.argv)
    pencere = LessonAttendance()
    pencere.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    lesson_attendance()