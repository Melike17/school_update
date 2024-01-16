import json
import csv
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

class User():
    FILE_PATH = "data/users.txt"
    ANNOUNCEMENT_FILE_PATH = "data/announcements.txt"

    _current_user= None
    FILE_LESSON = "data/lessons.csv"
    FILE_MENTOR = "data/mentors.csv"
    FILE_ATT_LESSON = "data/lesson_attendance.csv"
    FILE_ATT_MENTOR = "data/mentor_attendance.csv"
    table_lesson = None
    table_mentoring = None
    table_student = None
    
    def __init__(self, name, surname, email, birthdate, city, phone_number, password, user_type):
        self.name = name
        self.surname = surname
        self.email = email
        self.birthdate = birthdate
        self.city = city
        self.phone_number = phone_number
        self.password = password
        self.user_type = user_type

    @classmethod
    def create_user(cls, name, surname, email, birthdate, city, phone_number, password, user_type):
        # Check if the email already exists
        if cls.email_exists(email):
           QMessageBox.information(None, 'Warning', f'The email {email} already exists.', QMessageBox.Ok)
            
        else:
            new_user = cls(name, surname, email, birthdate, city, phone_number, password, user_type)
            cls.save_user(new_user.__dict__)
            # Show a success message
            QMessageBox.information(None, 'Success', 'User created successfully.', QMessageBox.Ok)
        
    @classmethod
    def email_exists(cls, email):
        existing_emails = cls.get_emails_for_task_assign()
        return email in existing_emails
    
    @classmethod
    def save_user(cls, user):
        try:
            with open(cls.FILE_PATH, 'a') as file:
                # Append the user data to the JSON file
                json.dump(user, file)
                file.write('\n')
            print("User saved to file.")
        except Exception as e:
            print(f"Error saving user to file: {e}")
    
    @classmethod
    def update_user_information(cls, email, **kwargs):
        try:
            # Read existing users
            with open(cls.FILE_PATH, 'r') as file:
                users = [json.loads(line) for line in file]

            # Find the user with the specified email
            for user in users:
                if user.get('email') == email:
                    # Update user information based on kwargs
                    user.update(kwargs)

            # Write the updated users back to the file
            with open(cls.FILE_PATH, 'w') as file:
                for user in users:
                    json.dump(user, file)
                    file.write('\n')

            print("User information updated.")
        except Exception as e:
            print(f"Error updating user information: {e}")

    @classmethod
    def get_emails_for_task_assign(cls):
        emails = []
        try:
            with open(cls.FILE_PATH, 'r') as file:
                for line in file:
                    user_data = json.loads(line)
                    emails.append(user_data.get('email'))
        except Exception as e:
            print(f"Error reading emails from file: {e}")
        return emails
    
    @classmethod
    def login(cls, email, password):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                for line in file:
                    user_data = json.loads(line)
                    if user_data.get('email') == email and user_data.get('password') == password:
                        return user_data
        except Exception as e:
            print(f"Error reading user data from file: {e}")
        return None
    
    @classmethod
    def set_currentuser(cls, email):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                for line in file:
                    user_data = json.loads(line)
                    if user_data.get('email') == email:
                        cls._current_user = cls(**user_data)
                        return
        except Exception as e:
            print(f"Error setting current user: {e}")

# Save the user information to the file
# User.create_user(
#     name="Student",
#     surname="Test",
#     email="student@example.com",
#     birthdate="1990-01-01",
#     city="Ist",
#     phone_number="123-456-7890",
#     password="12345",
#     user_type="student"
# )
    
    @classmethod
    def create_lessons(cls, lesson_info):
        try:
            rows = []
            flag = True

            if len(lesson_info) >= 4:
                with open(cls.FILE_LESSON, 'r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row and row[0] == lesson_info[0]:
                            row[1] = lesson_info[1]
                            row[2] = lesson_info[2]
                            row[3] = lesson_info[3]
                            flag = False
                        rows.append(row)
                    
                    if flag:
                        rows.append(lesson_info)
                
                with open(cls.FILE_LESSON, 'w', newline='') as file:
                    writer = csv.writer(file)

                    if not os.path.isfile(cls.FILE_LESSON):
                        writer.writerow(['Lesson Date','Lesson Name','Lesson Start Time','Lesson Finish Time'])
                    writer.writerows(rows)

        except Exception as e:
            print(f"Error in create lesson: {e}")


    @classmethod
    def get_LessonSchedule(cls):
        if cls.table_lesson is None: 
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(4)

        try:
            with open(cls.FILE_LESSON, 'r', newline='') as file:
                reader = csv.reader(file)
                cls.table_lesson.setRowCount(0)
                row_number = 0

                for row in reader:
                    cls.table_lesson.insertRow(row_number)
                    for column_number, info in enumerate(row):
                        cls.table_lesson.setItem(row_number, column_number, QTableWidgetItem(info))
                    row_number += 1
        
        except Exception as e:
            print(f"Error in getting lesson: {e}")

        return cls.table_lesson
    
    @classmethod
    def get_Lesson_Attendance(cls):
        if cls.table_lesson is None: 
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(2) 

        try:
            with open(cls.FILE_LESSON, 'r', newline='') as file:
                reader = csv.reader(file)
                cls.table_lesson.setRowCount(0)
                row_number = 0

                for row in reader:
                    if len(row) > 1:
                        cls.table_lesson.insertRow(row_number)
                        lesson_name = row[1]
                        cls.table_lesson.setItem(row_number, 0, QTableWidgetItem(lesson_name)) 
                        button = QPushButton("List")
                        button.clicked.connect(lambda _, lesson=lesson_name: cls.open_students_page_lesson(lesson))
                        cls.table_lesson.setCellWidget(row_number, 1, button) 
                        row_number += 1
            
        except Exception as e:
            print(f"Error in getting lesson: {e}")

        return cls.table_lesson
    
    @classmethod
    def get_Lesson_Attendance_Student(cls, email):
        if cls.table_lesson is None:
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(5)
        try:
            with open(cls.FILE_ATT_LESSON, 'r', newline='') as file:
                reader = csv.reader(file)
                cls.table_lesson.setRowCount(0)
                row_number = 0
                for row in reader:
                    if len(row) > 1 and row[1] == email:
                        cls.table_lesson.insertRow(row_number)
                        lesson_name, student_email, name, surname, attendance_status = row
                        cls.table_lesson.setItem(row_number, 0, QTableWidgetItem(name))
                        cls.table_lesson.setItem(row_number, 1, QTableWidgetItem(surname))
                        cls.table_lesson.setItem(row_number, 2, QTableWidgetItem(attendance_status))  # Değiştirildi
                        cls.table_lesson.setItem(row_number, 3, QTableWidgetItem(lesson_name))
                        cls.table_lesson.setItem(row_number, 4, QTableWidgetItem(student_email))  # Değiştirildi
                        row_number += 1
                        print(f"Row {row_number}: {name}, {surname}, {attendance_status}, {lesson_name}, {student_email}")
        except Exception as e:
            print(f"Error: {e}")
        return cls.table_lesson
    
    @classmethod
    def get_Mentor_Attendance_Student(cls, email):
        if cls.table_lesson is None:
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(5)
        try:
            with open(cls.FILE_ATT_MENTOR, 'r', newline='') as file:
                reader = csv.reader(file)
                cls.table_lesson.setRowCount(0)
                row_number = 0
                for row in reader:
                    if len(row) > 1 and row[1] == email:
                        cls.table_lesson.insertRow(row_number)
                        mentoring_name, student_email, name, surname, attendance_status = row
                        cls.table_lesson.setItem(row_number, 0, QTableWidgetItem(name))
                        cls.table_lesson.setItem(row_number, 1, QTableWidgetItem(surname))
                        cls.table_lesson.setItem(row_number, 2, QTableWidgetItem(attendance_status))  # Değiştirildi
                        cls.table_lesson.setItem(row_number, 3, QTableWidgetItem(mentoring_name))
                        cls.table_lesson.setItem(row_number, 4, QTableWidgetItem(student_email))  # Değiştirildi
                        row_number += 1
                        print(f"Row {row_number}: {name}, {surname}, {attendance_status}, {mentoring_name}, {student_email}")
        except Exception as e:
            print(f"Error: {e}")
        return cls.table_lesson
    
    @classmethod
    def get_Mentor_Attendance(cls):
        if cls.table_mentoring is None: 
            cls.table_mentoring = QTableWidget()
            cls.table_mentoring.setColumnCount(2) 

        try:
            with open(cls.FILE_MENTOR, 'r', newline='') as file:
                reader = csv.reader(file)
                cls.table_mentoring.setRowCount(0)
                row_number = 0

                for row in reader:
                    if len(row) > 1:
                        cls.table_mentoring.insertRow(row_number)
                        mentor_name = row[1]
                        cls.table_mentoring.setItem(row_number, 0, QTableWidgetItem(mentor_name)) 
                        button = QPushButton("List")
                        button.clicked.connect(lambda _, mentor=mentor_name: cls.open_students_page_mentor(mentor))
                        cls.table_mentoring.setCellWidget(row_number, 1, button) 
                        row_number += 1
            
        except Exception as e:
            print(f"Error in getting lesson: {e}")

        return cls.table_mentoring
    
    @classmethod
    def open_students_page_lesson(cls, item):
        selected_lesson = item
        students = cls.get_students()
        if students:
            cls.students_window = QWidget()
            cls.students_table = QTableWidget()
            cls.students_table.setColumnCount(4)
            cls.students_table.setRowCount(len(students))
            header = ["E-Mail","Name", "Surname", "Attendance"]
            cls.students_table.setHorizontalHeaderLabels(header)
            for i, column_name in enumerate(header):
                cls.students_table.setColumnWidth(i, 220)
            for row, (email, name, surname) in enumerate(students):
                cls.students_table.setRowHeight(row, 50)
            for row, (email, name, surname) in enumerate(students):
                cls.students_table.setItem(row, 0, QTableWidgetItem(email))
                cls.students_table.setItem(row, 1, QTableWidgetItem(name))
                cls.students_table.setItem(row, 2, QTableWidgetItem(surname))
                attended_btn = QPushButton("Attended")
                attended_btn.clicked.connect(lambda _, r=row: cls.mark_attendance_lesson(selected_lesson, r, "Attended"))
                attended_btn.setFixedWidth(100)
                not_attended_btn = QPushButton("Not Attended")
                not_attended_btn.clicked.connect(lambda _, r=row: cls.mark_attendance_lesson(selected_lesson, r, "Not Attended"))
                not_attended_btn.setFixedWidth(100)
                buttons_layout = QHBoxLayout()
                buttons_layout.addWidget(attended_btn)
                buttons_layout.addWidget(not_attended_btn)
                widget = QWidget()
                widget.setLayout(buttons_layout)
                cls.students_table.setCellWidget(row, 3, widget)
            layout = QVBoxLayout()
            layout.addWidget(cls.students_table)
            cls.students_window.setLayout(layout)
            cls.students_window.setWindowTitle(f"Students in {selected_lesson}")
            cls.students_window.show()
        else:
            QMessageBox.warning(cls, "No Students", "There are no students for this lesson.")


    @classmethod
    def mark_attendance_lesson(cls, lesson_name, row, attendance_status):
        student_email = cls.students_table.item(row, 0).text()
        student_name = cls.students_table.item(row, 1).text()
        student_surname = cls.students_table.item(row, 2).text()

        existing_lesson = False
        updated_students = []

        with open(cls.FILE_ATT_LESSON, newline="") as file:
            reader = csv.reader(file)
            for existing_row in reader:
                if existing_row[0] == lesson_name and existing_row[1] == student_email:
                    existing_lesson = True
                    existing_row[-1] = attendance_status
                updated_students.append(existing_row)

        if not existing_lesson:
            updated_students.append([lesson_name, student_email, student_name, student_surname, attendance_status])

        with open(cls.FILE_ATT_LESSON, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_students)
    
    
    @classmethod
    def open_students_page_mentor(cls, item):
        selected_mentor = item
        students = cls.get_students()
        if students:
            cls.students_window = QWidget()
            cls.students_table = QTableWidget()
            cls.students_table.setColumnCount(4)
            cls.students_table.setRowCount(len(students))
            header = ["E-Mail","Name", "Surname", "Attendance"]
            cls.students_table.setHorizontalHeaderLabels(header)
            for i, column_name in enumerate(header):
                cls.students_table.setColumnWidth(i, 220)
            for row, (email, name, surname) in enumerate(students):
                cls.students_table.setRowHeight(row, 50)
            for row, (email, name, surname) in enumerate(students):
                cls.students_table.setItem(row, 0, QTableWidgetItem(email))
                cls.students_table.setItem(row, 1, QTableWidgetItem(name))
                cls.students_table.setItem(row, 2, QTableWidgetItem(surname))
                attended_btn = QPushButton("Attended")
                attended_btn.clicked.connect(lambda _, r=row: cls.mark_attendance_mentor(selected_mentor, r, "Attended"))
                attended_btn.setFixedWidth(100)
                not_attended_btn = QPushButton("Not Attended")
                not_attended_btn.clicked.connect(lambda _, r=row: cls.mark_attendance_mentor(selected_mentor, r, "Not Attended"))
                not_attended_btn.setFixedWidth(100)
                buttons_layout = QHBoxLayout()
                buttons_layout.addWidget(attended_btn)
                buttons_layout.addWidget(not_attended_btn)
                widget = QWidget()
                widget.setLayout(buttons_layout)
                cls.students_table.setCellWidget(row, 3, widget)
            layout = QVBoxLayout()
            layout.addWidget(cls.students_table)
            cls.students_window.setLayout(layout)
            cls.students_window.setWindowTitle(f"Students in {selected_mentor}")
            cls.students_window.show()
        else:
            QMessageBox.warning(cls, "No Students", "There are no students for this lesson.")

    @classmethod
    def mark_attendance_mentor(cls, mentor_name, row, attendance_status):
       
        btn_widget = cls.students_table.cellWidget(row, 3)
        attended_btn = btn_widget.layout().itemAt(0).widget()
        not_attended_btn = btn_widget.layout().itemAt(1).widget()
        attended_btn.setEnabled(False)
        not_attended_btn.setEnabled(False)

        student_email = cls.students_table.item(row, 0).text()
        student_name = cls.students_table.item(row, 1).text()
        student_surname = cls.students_table.item(row, 2).text()

        existing_mentor = False
        updated_students = []

        with open(cls.FILE_ATT_MENTOR, newline="") as file:
            reader = csv.reader(file)
            for existing_row in reader:
                if existing_row[0] == mentor_name and existing_row[1] == student_email:
                    existing_mentor = True
                    existing_row[-1] = attendance_status
                updated_students.append(existing_row)

        if not existing_mentor:
            updated_students.append([mentor_name, student_email, student_name, student_surname, attendance_status])

        with open(cls.FILE_ATT_MENTOR, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_students)

    @classmethod
    def get_students(cls):
        students = []
        with open(cls.FILE_PATH, 'r') as file:
            data = file.readlines()
            for line in data:
                user_data = json.loads(line)
                if user_data.get('user_type') == 'student':
                    name = user_data.get('name')
                    surname = user_data.get('surname')
                    email = user_data.get('email')
                    students.append((email, name, surname))
        return students

    @classmethod
    def create_mentor(cls, mentor_info):
        try:
            rows = []
            flag = True
            if len(mentor_info) >= 4:
                with open(cls.FILE_MENTOR, 'r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row and row[0] == mentor_info[0]:
                            row[1] = mentor_info[1]
                            row[2] = mentor_info[2]
                            row[3] = mentor_info[3]
                            flag = False
                        rows.append(row)
                    
                    if flag:
                        rows.append(mentor_info)
                
                with open(cls.FILE_MENTOR, 'w', newline='') as file:
                    writer = csv.writer(file)

                    if not os.path.isfile(cls.FILE_MENTOR):
                        writer.writerow(['Mentoring Date','Mentoring Subject','Mentoring Start Time','Mentoring Finish Time'])
                    writer.writerows(rows)

        except Exception as e:
            print(f"Error in create mentoring: {e}")

    
    @classmethod
    def get_Mentor_Schedule(cls):
        if cls.table_mentoring is None: 
            cls.table_mentoring = QTableWidget()
            cls.table_mentoring.setColumnCount(4)

        try:
            with open(cls.FILE_MENTOR, 'r', newline='') as file:
                reader = csv.reader(file)
                cls.table_mentoring.setRowCount(0)
                row_number = 0

                for row in reader:
                    cls.table_mentoring.insertRow(row_number)
                    for column_number, info in enumerate(row):
                        cls.table_mentoring.setItem(row_number, column_number, QTableWidgetItem(info))
                    row_number += 1
        
        except Exception as e:
            print(f"Error in getting lesson: {e}")

        return cls.table_mentoring
    
    @classmethod
    def get_announcements(cls):
        announcements = []
        try:
            with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
                for line in file:
                    announcement_data = json.loads(line)
                    announcements.append(announcement_data)
            sorted_announcements = sorted(announcements, key=lambda x: x.get("timestamp"), reverse=True)

        except Exception as e:
            print(f"Error reading announcements from file: {e}")
        return sorted_announcements
    
    @classmethod
    def get_announcements_to_delete(cls, email, user_type):
        announcements = []
        try:
            with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
                for line in file:
                    announcement_data = json.loads(line)
                    created_by = announcement_data.get('created_by')
                    # Check user type and email conditions
                    if (user_type == "admin") or (user_type == "teacher" and created_by == email):
                        announcements.append(announcement_data)
        except Exception as e:
            print(f"Error reading announcements from file: {e}")
        return announcements
    
    @classmethod
    def delete_announcement(cls, text):
        try:
            # Read existing announcements
            with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
                announcements = [json.loads(line) for line in file]

            # Find and remove the announcement based on the name
            updated_announcements = [announcement for announcement in announcements
                                    if announcement.get('announcement') != text]

            # Write the updated announcements back to the file
            with open(cls.ANNOUNCEMENT_FILE_PATH, 'w') as file:
                for announcement in updated_announcements:
                    json.dump(announcement, file)
                    file.write('\n')

            print(f"Announcement '{text}' deleted.")
        except Exception as e:
            print(f"Error deleting announcement: {e}")

    @classmethod
    def create_announcement(cls, announcement, created_by):
        try:
            # Read existing announcements
            with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
                existing_announcements = [json.loads(line) for line in file]

            # Check if the announcement with the same name already exists
            if any(existing_announcement['announcement'] == announcement for existing_announcement in existing_announcements):
                return False, "Error: Announcement with the same name already exists."

            # Append the announcement data to the JSON file
            with open(cls.ANNOUNCEMENT_FILE_PATH, 'a') as file:
                announcement_data = {
                    'announcement': announcement,
                    'created_by': created_by,
                    'timestamp': QDateTime.currentDateTime().toString(Qt.ISODate)
                }
                json.dump(announcement_data, file)
                file.write('\n')
            
            return True, "Announcement created"
        except Exception as e:
            print(f"Error creating announcement: {e}")
        




