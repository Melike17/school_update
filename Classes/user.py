import sys,os
sys.path.append(os.getcwd())
import json
import csv
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from db_connect import get_db_connection
import logging

class User():
    
    logFile = 'data/logging.log'
    logFormat = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=logFile, level=logging.DEBUG, format=logFormat)

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
    
    def __init__(self, name, last_name, email, birthdate, city, phone_number, password, user_type,status, avatar_path):
        self.name = name
        self.surname = last_name
        self.email = email
        self.birthdate = birthdate
        self.city = city
        self.phone_number = phone_number
        self.password = password
        self.user_type = user_type
        self.status=status
        self.avatar_path = avatar_path

    @classmethod
    def create_user(cls, name, last_name, email, birthdate, city, phone_number, password, user_type,status, avatar_path):
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    if cls.email_exists(email):
                        QMessageBox.information(None, 'Warning', f'The email {email} already exists.', QMessageBox.Ok)
                   
                    else:
                        
                        #avatar_path_random=random(["cat.png","koala.png"])
                        avatar_path="avatars/cat.png"
                        
                        query = """
                            INSERT INTO school.user (name, last_name, email, birthdate, city, phone_number, password_hash, user_type,status,avatar_path)
                            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
                            RETURNING user_id
                        """
                        cursor.execute(query, (name, last_name, email, birthdate, city, phone_number, password, user_type,status,avatar_path))
                        # Show a success message
                        conn.commit()
                        QMessageBox.information(None, 'Success', 'User created successfully.', QMessageBox.Ok)
                    
            except Exception as e:
                print(f"Error: {e}")
            
        
            
        
        
    @classmethod
    def email_exists(cls, email):
        existing_emails = cls.get_emails_for_task_assign()
        return email in existing_emails
    
    # @classmethod
    # def save_user(cls, user):
    #     try:
    #         with open(cls.FILE_PATH, 'a') as file:
    #             # Append the user data to the JSON file
    #             json.dump(user, file)
    #             file.write('\n')
    #         print("User saved to file.")
    #     except Exception as e:
    #         print(f"Error saving user to file: {e}")
    
    @classmethod
    def update_user_information(cls, email, **kwargs):
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    # Update user information based on kwargs
                    update_query = "UPDATE school.user SET "
                    values = []
                    for key, value in kwargs.items():
                        update_query += f"{key} = %s, "
                        values.append(value)
                    update_query = update_query.rstrip(", ")  # Remove the trailing comma
                    update_query += " WHERE email = %s"
                    values.append(email)

                    cursor.execute(update_query, tuple(values))
                    conn.commit()

                    #QMessageBox.information(None, 'Success', 'User information updated successfully.', QMessageBox.Ok)

            except Exception as e:
                print(f"Error updating user information: {e}")

    @classmethod
    def get_emails_for_task_assign(cls):
        emails = []
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = "SELECT email FROM school.user"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    emails = [row[0] for row in result]
        except Exception as e:
            print(f"Error retrieving emails from the database: {e}")

        return emails

    
    @classmethod
    def login(cls, email, password):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''
                    SELECT name, last_name, email, birthdate, city, phone_number, password_hash, user_type, status, avatar_path
                    FROM school.user
                    WHERE email = %s AND password_hash = %s
                    
                    '''
                    
                    cursor.execute(query, (email, password))
                    result = cursor.fetchone()
                    # Print the result for debugging
                    #print("Query Result:", result)
                    
                    if result:
                        user_data = {
                            "name": result[0],
                            "last_name": result[1],
                            "email": result[2],
                            "birthdate": result[3],
                            "city": result[4],
                            "phone_number": result[5],
                            "password_hash": result[6],
                            "user_type": result[7],
                            "status": result[8],
                            "avatar_path":result[9]
                        }
                        return user_data
        except Exception as e:
            print(f"Error reading user data from the database: {e}")
        return None

        

    @classmethod
    def set_currentuser(cls, email):
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = '''
                    SELECT name, last_name, email, birthdate, city, phone_number, password_hash, user_type, status, avatar_path
                    FROM school.user WHERE email = %s
                    '''
                    cursor.execute(sql_query, (email,))
                    user_data = cursor.fetchone()
                    if user_data:
                        # Unpack the user_data tuple and create a User instance
                        user_instance = cls(*user_data)
                        cls._current_user = user_instance
                        return
            except Exception as e:
                print(f"Error setting current user: {e}")
                
   
                
    @classmethod
    def get_teachers_by_status(cls, status):
        teachers = []
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    sql_query = '''
                    SELECT name, email, status
                    FROM school.user
                    WHERE user_type = 'teacher' AND status = %s
                    '''
                    cursor.execute(sql_query, (status,))
                    teachers = cursor.fetchall()

        except Exception as e:
            print(f"Error getting teachers by status: {e}")
            
        teachers_with_options = [(name, email, status, 'Approve', 'Reject') for name, email, status in teachers]
        return teachers
                
    #---------------------------------------------------------------------------------------



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
    def create_lessons(cls, email, lesson_info):
        try:
            date, lesson, start, finish = lesson_info

            with get_db_connection() as conn:
                try:
                    with conn.cursor() as cursor:
                        
                        cursor.execute("SELECT user_id FROM school.user WHERE email = %s", (email,))
                        user_id = cursor.fetchone()[0]

                        
                        cursor.execute('''
                            INSERT INTO school.mentoringlesson (name, date, start, finish, type, user_id)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (lesson, date, start, finish, 'lesson', user_id))

                        logging.info(f"Lesson created successfully by email {email}: {lesson_info}")            
                except Exception as e:
                    print(f"Error in create lesson: {e}")

        except Exception as e:
            print(f"Error in create lesson: {e}")


    @classmethod
    def get_LessonSchedule(cls):

        if cls.table_lesson is None: 
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(4)

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name, date, start, finish FROM school.mentoringlesson WHERE type = 'lesson'")
                    lessons = cursor.fetchall()

                    cls.table_lesson.setRowCount(0)

                    for row_number, lesson in enumerate(lessons):
                        cls.table_lesson.insertRow(row_number)
                        for column_number, info in enumerate(lesson):
                            cls.table_lesson.setItem(row_number, column_number, QTableWidgetItem(str(info)))

            except Exception as e:
                print(f"Error: {e}")

        return cls.table_lesson
    
    @classmethod
    def get_Lesson_Attendance(cls):
        if cls.table_lesson is None: 
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(2) 

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name FROM school.mentoringlesson WHERE type = 'lesson'") 
                    lessons = cursor.fetchall()
                    cls.table_lesson.setRowCount(0)

                    for row_number, lesson in enumerate(lessons):
                        cls.table_lesson.insertRow(row_number)
                        for column_number, info in enumerate(lesson):
                            cls.table_lesson.setItem(row_number, column_number, QTableWidgetItem(str(info)))

                        list_button = QPushButton("List")
                        list_button.clicked.connect(lambda _, lesson_name=lesson[0]: cls.open_students_page_lesson(lesson_name))
                        cls.table_lesson.setCellWidget(row_number, 2, list_button)
            
            except Exception as e:
                print(f"Error in getting lesson: {e}")

        return cls.table_lesson
    
    @classmethod
    def get_Lesson_Attendance_Student(cls, email):
        if cls.table_lesson is None:
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(4)

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        SELECT us.name, us.last_name, att.status, ml.name 
                        FROM school.user AS us
                        JOIN school.attendance AS att ON us.user_id = att.user_id
                        JOIN school.mentoringlesson AS ml ON att.mentoringlesson_id = ml.id
                        WHERE ml.type = 'lesson' AND us.email = %s
                    ''', (email,))
                    lessons = cursor.fetchall()

                    cls.table_lesson.setRowCount(0)

                    for row_number, lesson in enumerate(lessons):
                        cls.table_lesson.insertRow(row_number)
                        for column_number, info in enumerate(lesson):
                            cls.table_lesson.setItem(row_number, column_number, QTableWidgetItem(str(info)))

            except Exception as e:
                print(f"Error: {e}")

        return cls.table_lesson
    
    @classmethod
    def get_Mentor_Attendance_Student(cls, email):
        if cls.table_mentoring is None:
            cls.table_mentoring = QTableWidget()
            cls.table_mentoring.setColumnCount(4)
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        SELECT us.name, us.last_name, att.status, ml.name 
                        FROM school.user AS us
                        JOIN school.attendance AS att ON us.user_id = att.user_id
                        JOIN school.mentoringlesson AS ml ON att.mentoringlesson_id = ml.id
                        WHERE ml.type = 'mentor' AND us.email = %s
                    ''', (email,))
                    mentors = cursor.fetchall()

                    cls.table_mentoring.setRowCount(0)

                    for row_number, mentor in enumerate(mentors):
                        cls.table_mentoring.insertRow(row_number)
                        for column_number, info in enumerate(mentor):
                            cls.table_mentoring.setItem(row_number, column_number, QTableWidgetItem(str(info)))

            except Exception as e:
                print(f"Error: {e}")
        return cls.table_mentoring
    
    @classmethod
    def get_Mentor_Attendance(cls):
        if cls.table_mentoring is None: 
            cls.table_mentoring = QTableWidget()
            cls.table_mentoring.setColumnCount(2) 

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name FROM school.mentoringlesson WHERE type = 'mentor'") 
                    mentors = cursor.fetchall()
                    cls.table_mentoring.setRowCount(0)

                    for row_number, mentor in enumerate(mentors):
                        cls.table_mentoring.insertRow(row_number)
                        for column_number, info in enumerate(mentor):
                            cls.table_mentoring.setItem(row_number, column_number, QTableWidgetItem(str(info)))

                        list_button = QPushButton("List")
                        list_button.clicked.connect(lambda _, lesson_name=mentor[0]: cls.open_students_page_lesson(lesson_name))
                        cls.table_mentoring.setCellWidget(row_number, 2, list_button)
            
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
        btn_widget = cls.students_table.cellWidget(row, 3)
        attended_btn = btn_widget.layout().itemAt(0).widget()
        not_attended_btn = btn_widget.layout().itemAt(1).widget()
        attended_btn.setEnabled(False)
        not_attended_btn.setEnabled(False)

        student_email = cls.students_table.item(row, 0).text()

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT user_id FROM school.user WHERE email = %s", (student_email,))
                    user_data = cursor.fetchone()
                    if user_data:
                        user_id = user_data[0]
                        cursor.execute("SELECT id FROM school.mentoringlesson WHERE name = %s", (lesson_name,))
                        lesson_data = cursor.fetchone()
                        if lesson_data:
                            lesson_id = lesson_data[0]
                            cursor.execute('''
                                INSERT INTO school.attendance (mentoringlesson_id, user_id, status)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (mentoringlesson_id, user_id) DO UPDATE SET status = %s
                            ''', (lesson_id, user_id, attendance_status, attendance_status))
                        else:
                            print(f"Lesson with name {lesson_name} not found.")
                    else:
                        print(f"User with email {student_email} not found.")

            except Exception as e:
                print(f"Error in marking attendance: {e}")
    
    
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

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT user_id FROM school.user WHERE email = %s", (student_email,))
                    user_data = cursor.fetchone()
                    if user_data:
                        user_id = user_data[0]
                        cursor.execute("SELECT id FROM school.mentoringlesson WHERE name = %s", (mentor_name,))
                        mentor_data = cursor.fetchone()
                        if mentor_data:
                            lesson_id = mentor_data[0]
                            cursor.execute('''
                                INSERT INTO school.attendance (mentoringlesson_id, user_id, status)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (mentoringlesson_id, user_id) DO UPDATE SET status = %s
                            ''', (lesson_id, user_id, attendance_status, attendance_status))
                        else:
                            print(f"Lesson with name {mentor_name} not found.")
                    else:
                        print(f"User with email {student_email} not found.")

            except Exception as e:
                print(f"Error in marking attendance: {e}")

    @classmethod
    def get_students(cls):
        students = []

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT email, name, last_name FROM school.user WHERE user_type = 'student'")
                    student_records = cursor.fetchall()

                    for record in student_records:
                        email, name, surname = record
                        students.append((email, name, surname))

            except Exception as e:
                print(f"Error in getting students: {e}")

        return students
    
    @classmethod
    def get_lesson_names(cls):
        lesson_names = []

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name FROM school.mentoringlesson WHERE type = 'lesson'")
                    lessons = cursor.fetchall()

                    for lesson in lessons:
                        lesson_names.append(lesson[0])

            except Exception as e:
                print(f"Error in getting lesson names: {e}")

        return lesson_names
    
    @classmethod
    def get_lesson_names(cls):
        mentor_names = []

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name FROM school.mentoringlesson WHERE type = 'mentor'")
                    mentors = cursor.fetchall()

                    for mentor in mentors:
                        mentor_names.append(mentor[0])

            except Exception as e:
                print(f"Error in getting mentor names: {e}")

        return mentor_names

    @classmethod
    def create_mentor(cls, email, mentor_info):
        try:
            date, mentor, start, finish = mentor_info

            with get_db_connection() as conn:
                try:
                    with conn.cursor() as cursor:
                        
                        cursor.execute("SELECT user_id FROM school.user WHERE email = %s", (email,))
                        user_id = cursor.fetchone()[0]

                        
                        cursor.execute('''
                            INSERT INTO school.mentoringlesson (name, date, start, finish, type, user_id)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (mentor, date, start, finish, 'mentor', user_id))

                        logging.info(f"Mentor created successfully by {email}: {mentor_info}")            
                except Exception as e:
                    print(f"Error in create mentor: {e}")

        except Exception as e:
            print(f"Error in create mentor: {e}")

    
    @classmethod
    def get_Mentor_Schedule(cls):
        if cls.table_mentoring is None: 
            cls.table_mentoring = QTableWidget()
            cls.table_mentoring.setColumnCount(4)

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name, date, start, finish FROM school.mentoringlesson WHERE type = 'mentor'")
                    mentors = cursor.fetchall()

                    cls.table_mentoring.setRowCount(0)

                    for row_number, lesson in enumerate(mentors):
                        cls.table_mentoring.insertRow(row_number)
                        for column_number, info in enumerate(lesson):
                            cls.table_mentoring.setItem(row_number, column_number, QTableWidgetItem(str(info)))

            except Exception as e:
                print(f"Error: {e}")

        return cls.table_mentoring
    
    # @classmethod
    # def get_announcements(cls):
    #     announcements = []
    #     try:
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
    #             for line in file:
    #                 announcement_data = json.loads(line)
    #                 announcements.append(announcement_data)
    #         sorted_announcements = sorted(announcements, key=lambda x: x.get("timestamp"), reverse=True)

    #     except Exception as e:
    #         print(f"Error reading announcements from file: {e}")
    #     return sorted_announcements
    @classmethod
    def get_announcements(cls):
        announcements = []
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''
                        SELECT user_id, expression, expiry_date
                        FROM school.duyuru
                        ORDER BY expiry_date DESC
                    '''
                    cursor.execute(query)
                    result = cursor.fetchall()

                    for row in result:
                        announcement_data = {
                            "user_id": row[0],
                            "announcement": row[1],
                            "expiry_date": QDateTime.fromString(row[2], Qt.ISODate).toString(Qt.ISODate),  
                            #"due_date":row[3].isoformat()
                        }
                        announcements.append(announcement_data)

        except Exception as e:
            print(f"Error reading announcements from database: {e}")

        return announcements
    
    # @classmethod
    # def get_announcements_to_delete(cls, email, user_type):
    #     announcements = []
    #     try:
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
    #             for line in file:
    #                 announcement_data = json.loads(line)
    #                 created_by = announcement_data.get('created_by')
    #                 # Check user type and email conditions
    #                 if (user_type == "admin") or (user_type == "teacher" and created_by == email):
    #                     announcements.append(announcement_data)
    #     except Exception as e:
    #         print(f"Error reading announcements from file: {e}")
    #     return announcements
    @classmethod
    def get_announcements_to_delete(cls, email, user_type):
        announcements = []
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Find user_id associated with the given email
                    user_query = "SELECT user_id FROM school.user WHERE email = %s"
                    cursor.execute(user_query, (email,))
                    user_id = cursor.fetchone()[0] if email else None
                    query = '''
                        SELECT user_id, expression, expiry_date
                        FROM school.duyuru
                    '''
                    cursor.execute(query)
                    result = cursor.fetchall()

                    for row in result:
                        announcement_data = {
                            "user_id": row[0],
                            "announcement": row[1],
                            "expiry_date": QDateTime.fromString(row[2], Qt.ISODate).toString(Qt.ISODate),
                            #"due_date": row[3].isoformat()
                        }
                        # Check user type and email conditions
                        if (user_type == "admin") or (user_type == "teacher" and announcement_data["user_id"] == user_id):
                            announcements.append(announcement_data)

        except Exception as e:
            print(f"Error reading announcements from database: {e}")

        return announcements

    
    # @classmethod
    # def delete_announcement(cls, text):
    #     try:
    #         # Read existing announcements
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
    #             announcements = [json.loads(line) for line in file]

    #         # Find and remove the announcement based on the name
    #         updated_announcements = [announcement for announcement in announcements
    #                                 if announcement.get('announcement') != text]

    #         # Write the updated announcements back to the file
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'w') as file:
    #             for announcement in updated_announcements:
    #                 json.dump(announcement, file)
    #                 file.write('\n')

    #         print(f"Announcement '{text}' deleted.")
    #     except Exception as e:
    #         print(f"Error deleting announcement: {e}")
    @classmethod
    def delete_announcement(cls, text):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Delete announcement from the database
                    query = '''
                        DELETE FROM school.duyuru
                        WHERE expression = %s
                    '''
                    cursor.execute(query, (text,))
                    conn.commit()

            print(f"Announcement '{text}' deleted from the database.")
        except Exception as e:
            print(f"Error deleting announcement: {e}")


    # @classmethod
    # def create_announcement(cls, announcement, created_by):
    #     try:
    #         # Read existing announcements
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
    #             existing_announcements = [json.loads(line) for line in file]

    #         # Check if the announcement with the same name already exists
    #         if any(existing_announcement['announcement'] == announcement for existing_announcement in existing_announcements):
    #             return False, "Error: Announcement with the same name already exists."

    #         # Append the announcement data to the JSON file
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'a') as file:
    #             announcement_data = {
    #                 'announcement': announcement,
    #                 'created_by': created_by,
    #                 'timestamp': QDateTime.currentDateTime().toString(Qt.ISODate)
    #             }
    #             json.dump(announcement_data, file)
    #             file.write('\n')
            
    #         return True, "Announcement created"
    #     except Exception as e:
    #         print(f"Error creating announcement: {e}")
    
    @classmethod
    def create_announcement(cls, announcement, created_by):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    user_query = "SELECT user_id FROM school.user WHERE email = %s"
                    cursor.execute(user_query, (cls._current_user.email,))
                    user_id = cursor.fetchone()[0] if cls._current_user else None
                    # Insert announcement into the database
                    query = f'''
                        INSERT INTO school.duyuru
                        (user_id, expression, expiry_date) 
                        VALUES (%s, %s, %s)
                    '''
                    expiry_date = QDateTime.currentDateTime().toString(Qt.ISODate)
                    cursor.execute(query, (user_id, announcement,  expiry_date))
                    conn.commit()

            return True, "Announcement created"
        except Exception as e:
            print(f"Error creating announcement: {e}")
            return False, f"Error creating announcement: {e}"






