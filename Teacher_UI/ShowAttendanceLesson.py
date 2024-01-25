import csv
import sys
import os
sys.path.append(os.getcwd())
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QComboBox
from db_connect import get_db_connection
import logging

class ShowAttLesson(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance Information")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(self.get_distinct_lesson_names())
        self.filter_combo.currentIndexChanged.connect(self.update_table)
        layout.addWidget(self.filter_combo)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.update_table(0)

    def get_distinct_lesson_names(self):
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT name FROM school.mentoringlesson WHERE type = 'lesson'")
                    lesson_names = [row[0] for row in cursor.fetchall()]
                    return lesson_names
            except Exception as e:
                print(f"Error fetching lesson names: {e}")
                return []

    def update_table(self, index):
        current_text = self.filter_combo.currentText()

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    # Get users who attended the selected lesson
                    cursor.execute('''
                        SELECT us.name, us.last_name, att.status
                        FROM school.user as us
                        JOIN school.attendance as att ON us.user_id = att.user_id
                        JOIN school.mentoringlesson as men ON att.mentoringlesson_id = men.id
                        WHERE men.name = %s AND men.type = 'lesson'
                    ''', (current_text,))
                    filtered_data = cursor.fetchall()
                    print( "filtered data", filtered_data)
            except Exception as e:
                print(f"Error fetching data: {e}")
                filtered_data = []

        self.table_widget.clear()
        self.table_widget.setRowCount(len(filtered_data))
        self.table_widget.setColumnCount(len(filtered_data[0]))

        headers = [desc[0] for desc in cursor.description]
        self.table_widget.setHorizontalHeaderLabels(headers)

        for i, row_data in enumerate(filtered_data):
            for j, info in enumerate(row_data):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(info)))

def show_attendance_ui():
    app = QApplication([])
    window = ShowAttLesson()
    window.show()
    app.exec_()

#show_attendance_ui()