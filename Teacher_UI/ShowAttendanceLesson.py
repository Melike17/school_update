import csv
import sys
import os
sys.path.append(os.getcwd())
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QComboBox

def read_csv(file_path):
    table_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table_data.append(row)
    return table_data

class ShowAttLesson(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance Information")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.data = read_csv(file_path)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(list(set(entry['Lesson Name'] for entry in self.data)))
        self.filter_combo.currentIndexChanged.connect(self.update_table)
        layout.addWidget(self.filter_combo)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.update_table(0)

    def update_table(self, index):
        current_text = self.filter_combo.currentText()
        filtered_data = [entry for entry in self.data if entry['Lesson Name'] == current_text]

        self.table_widget.clear()
        self.table_widget.setRowCount(len(filtered_data))
        self.table_widget.setColumnCount(len(filtered_data[0]))

        headers = list(filtered_data[0].keys())
        self.table_widget.setHorizontalHeaderLabels(headers)

        for i, row_data in enumerate(filtered_data):
            for j, key in enumerate(headers):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(row_data[key])))


def show_attendance_ui(file_path):
    app = QApplication([])
    window = ShowAttLesson()
    window.show()
    app.exec_()

file_path = "data/lesson_attendance.csv"
#show_attendance_ui(file_path)