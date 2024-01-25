import sys
import os
import re
from pathlib import Path
sys.path.append(os.getcwd())
import logging
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Teacher_UI.Ui_teacher_v1 import *
from Classes.task import Task
from Classes.user import *
from Teacher_UI.CreateLesson import *
from Teacher_UI.CreateMentor import *
from Teacher_UI.LessonAttendance import *
from Teacher_UI.MentorAttendance import *
from Teacher_UI.ShowAttendanceLesson import *
from Teacher_UI.ShowAttendanceMentor import *
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget, QLabel, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QPixmap, QBitmap, QFont, QPainter
from PyQt5.QtCore import Qt
from Chat_UI.chat_mobile import MainWindow as Chat_Main_Window


class TeacherUserListItemWidget(QWidget):
    def __init__(self, user_id, user_name, last_name, user_type, avatar_path):
        super(TeacherUserListItemWidget, self).__init__()

        layout = QHBoxLayout(self)

        # Avatar Label
        avatar_label = QLabel(self)
        avatar_pixmap = QPixmap(avatar_path).scaledToWidth(30).scaledToHeight(30, Qt.SmoothTransformation)

        # Circular mask for the avatar
        mask = QBitmap(avatar_pixmap.size())
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, mask.width(), mask.height())
        painter.end()

        avatar_pixmap.setMask(mask)
        avatar_label.setPixmap(avatar_pixmap)
        avatar_label.setFixedSize(30, 30)
        avatar_label.setScaledContents(True)
        layout.addWidget(avatar_label)

        # User information labels
        user_name_label = QLabel(f"{user_name} {last_name}")
        layout.addWidget(user_name_label)

        user_type_label = QLabel(user_type)
        user_type_label.setFont(QFont("Arial", italic=True))
        layout.addWidget(user_type_label)

        # Set layout margins and spacing
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Set user_id as custom data
        self.user_id = user_id
        # Set the background color to transparent initially
        self.setStyleSheet("background-color: transparent;")


class Teacher_Main_Window(QMainWindow, Ui_MainWindow):


    def __init__(self):
        super(Teacher_Main_Window,self).__init__()

        #User.set_currentuser("teacher@example.com")
        self.ui = uic.loadUi('Teacher_UI/teacher_v1.ui', self)

        self.setupUi(self)
        self.setWindowTitle("Teacher Page")

        avatar_pixmap = QPixmap(User._current_user.avatar_path).scaledToWidth(60).scaledToHeight(60, Qt.SmoothTransformation)

        # Circular mask for the avatar
        mask = QBitmap(avatar_pixmap.size())
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, mask.width(), mask.height())
        painter.end()

        avatar_pixmap.setMask(mask)
        self.user_avatar.setPixmap(avatar_pixmap)
        self.user_avatar.setFixedSize(60, 60)
        self.user_avatar.setScaledContents(True)

        

        
        self.current_user_email = User._current_user.email

        #hide admin tab if user is not admin
        tab_widget = self.tabWidget
        if User._current_user.user_type != "admin":
            tab_widget.removeTab(6)
        else:
            self.display_status()
        tab_widget.removeTab(5)
        
        # Create a QTimer instance
        self.timer = QTimer(self)
        # Connect the timeout signal of the timer to your update_announcements function
        self.timer.timeout.connect(self.update_announcements)
        # Set the timeout interval to 5000 milliseconds (5 seconds)
        self.timer.start(1000)
        # Initialize a counter to keep track of the current announcement
        self.current_announcement_index = 0

        #self.display_announcements()
        self.display_announcement_to_delete()
        self.show_user_list_for_task()

        current_date_time = QDateTime.currentDateTime()
        formatted_date = current_date_time.toString("dd-MM-yyyy")
        self.teacher_main_name.setText(f" {User._current_user.name}")
        self.teacher_main_date.setText(f"{formatted_date}")

        self.show_information()
        
        self.load_tasks()
        #initial values of task create form
        #self.assignee_input_combo.addItem("")
        #self.assignee_input_combo.addItems(User.get_emails_for_task_assign())
        #self.due_date_input.setDate(QtCore.QDate(1000, 1, 1))

        #signal to create task button
        self.create_task_button.clicked.connect(self.create_task)
        self.due_date_input.setMinimumDate(QDate.currentDate())
        self.tasks_tableWidget.setStyleSheet("") 

        #signal to create teacher account
        #self.create_teacher_account_button.clicked.connect(self.check_enter_signup)

        self.show_Lesson_Schedule()
        self.show_Mentor_Schedule()

        self.create_lesson.clicked.connect(self.open_create_lesson)
        self.create_mentor.clicked.connect(self.open_create_mentor)
        self.update_lessons.clicked.connect(self.refresh_lesson)
        self.update_mentoring.clicked.connect(self.refresh_mentor)

        self.lesson_att_insert.clicked.connect(self.show_lesson_attendance_page)
        self.mentor_att_insert.clicked.connect(self.show_mentor_attendance_page)
        self.lesson_att_show.clicked.connect(self.show_lesson_attendance_show)
        self.mentor_att_show.clicked.connect(self.show_mentor_attendance_show)

        self.create_announcement_button.clicked.connect(self.create_announcement)
        self.delete_announcement_button.clicked.connect(self.delete_announcement)

        self.update_information_button.clicked.connect(self.update_information)

        self.selected_user_ids = []
        self.task_user_list.itemSelectionChanged.connect(self.handle_selection_change)

        self.tabWidget.setCurrentIndex(0)

        self.chat_teacher_button.clicked.connect(self.open_chat)

    def open_chat(self):
        if not hasattr(self, 'ui_main_4') or not self.ui_main_4.isVisible():
            # If ui_main_4 is not defined or is not visible, create and show it
            self.ui_main_4 = QtWidgets.QMainWindow()
            self.ui_main_4 = Chat_Main_Window()
            self.ui_main_4.show()
        else:
            # If ui_main_4 is already visible, bring it to the front
            self.ui_main_4.raise_()
            self.ui_main_4.activateWindow()

    def handle_selection_change(self):
        self.selected_user_ids = []
        for item in self.task_user_list.selectedItems():
            user_item_widget = self.task_user_list.itemWidget(item)
            if user_item_widget:
                self.selected_user_ids.append(user_item_widget.user_id)

        print("Selected User IDs:", self.selected_user_ids)    

    def update_information(self):
        self.teacher_profil_tel_edit = self.findChild(QtWidgets.QTextEdit,"teacher_profil_tel_edit")
        self.teacher_profil_city_edit = self.findChild(QtWidgets.QTextEdit,"teacher_profil_city_edit")

        new_tel = self.teacher_profil_tel_edit.toPlainText()
        new_city = self.teacher_profil_city_edit.toPlainText()
        updated_info = {"phone_number": new_tel, "city": new_city  }
        User.update_user_information(User._current_user.email, **updated_info)
        self.showUpdateAlert("Information is updated")
        #Add log file
        logging.info(f"Information updated by {User._current_user.name}") 

    #--------------- Create Teacher Account------------------
    def check_enter_signup(self):
        self.teacher_name_admin = self.findChild(QtWidgets.QLineEdit, "teacher_name_admin")
        self.teache_surname_admin = self.findChild(QtWidgets.QLineEdit, "teache_surname_admin")
        self.teacher_city_admin = self.findChild(QtWidgets.QLineEdit, "teacher_city_admin")
        self.teacher_email_admin = self.findChild(QtWidgets.QLineEdit, "teacher_email_admin")
        self.teacher_tel_admin = self.findChild(QtWidgets.QLineEdit, "teacher_tel_admin")
        self.teacher_password_admin = self.findChild(QtWidgets.QLineEdit, "teacher_password_admin")
        self.teacher_birthdate_admin = self.findChild(QtWidgets.QDateEdit, "teacher_birthdate_admin")

        name = self.teacher_name_admin.text()
        surname = self.teache_surname_admin.text()
        birthday = self.teacher_birthdate_admin.date().toString(QtCore.Qt.ISODate) #ISO standart for Date
        city = self.teacher_city_admin.text()
        email = self.teacher_email_admin.text()
        phone_number=self.teacher_tel_admin.text()
        password = self.teacher_password_admin.text()
        if (name == '' or surname == '' or birthday=='' or city == '' or email == '' or password == ''):
            self.ui_main_3_window.statusBar().showMessage("Please fill in the blanks!", 2000)
        elif not self.is_valid_email(email):
            self.ui_main_3_window.statusBar().showMessage("Please enter a valid email address!", 2000)
        elif not self.is_valid_password(password):
            self.ui_main_3_window.statusBar().showMessage("Please enter a valid password!", 2000)
        else:
            self.create_Teacher(name, surname,email, birthday, city,phone_number, password)

    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email)
    
    def is_valid_password(self,password):
        password = self.teacher_password_admin.text()

        if len(password) <= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password) and any(c.isascii() and not c.isalnum() for c in password):
            return True
        else:
            return False
    
    def create_Teacher(self,name, surname, email, birthday, city,phone_number, password):
        if not User.email_exists(email):
            User.create_user(name, surname, email, birthday, city, phone_number, password, user_type="teacher")
            print("User created successfully.")
        else:
            QMessageBox.warning(None, 'Warning', f'The email {email} already exists.', QMessageBox.Ok)

    #-----------------------------------------------------------------
    # def display_status(self):
    #     try:
           
    #         # Take the teachers by status
    #         passive_teachers = User.get_teachers_by_status('passive')
    #         print(passive_teachers)
    #         # Show in ListWidget
    #         list_widget = self.findChild(QListWidget, "listWidget")
    #         list_widget.clear()

    #         for teacher in passive_teachers:
    #             print("Current Teacher:", teacher)
    #             item_text = f"{teacher[0]} {teacher[1]} ({teacher[2]})"
    #             print("Item Text:", item_text)
    #             item = QtWidgets.QListWidgetItem(item_text)
    #             list_widget.addItem(item)


    #     except Exception as e:
    #         print(f"Error displaying teachers with 'passive' status: {e}")
    def display_status(self):
        try:
            # Take the teachers by status
            passive_teachers = User.get_teachers_by_status('passive')
            print(passive_teachers)
            # List widget
            list_widget = self.findChild(QListWidget, "listWidget")
            list_widget.clear()
            

            # Add teachers to list widget
            for teacher in passive_teachers:
                item_text = f"Name: {teacher[0]}, Email: {teacher[1]}, Status: {teacher[2]}"
                item = QListWidgetItem(item_text)
                list_widget.addItem(item)

            # Your custom reject and approve buttons
            reject_button = self.reject_Button
            approve_button = self.approve_Button
            

            # Connect buttons to functions
            approve_button.clicked.connect(self.approve_teacher)
            reject_button.clicked.connect(self.reject_teacher)

                
        except Exception as e:
            print(f"Error displaying teachers with 'passive' status: {e}")

    def approve_teacher(self):
        selected_item = self.findChild(QListWidget, "listWidget").currentItem()
        print(selected_item.text())
        # Extracting teacher email from the selected item's text
        
        if selected_item is not None:
            email = selected_item.text().split(",")[1].split(":")[1].strip()
            # Update the teacher status to 'active' in the database
            self.update_teacher_status(email, 'active')
            # Remove the item from the list widget   
            selected_row = self.findChild(QListWidget, "listWidget").row(selected_item)
            self.findChild(QListWidget, "listWidget").takeItem(selected_row)
            # Success Message
            QMessageBox.information(self, "Warning", "Teacher status changed successfully!")
            #Add log file
            logging.info(f"One teacher account approved by {User._current_user.name}") 

    def reject_teacher(self):
        selected_item = self.findChild(QListWidget, "listWidget").currentItem()
        print(selected_item.text())
        
        if selected_item is not None:
            try:
                email = selected_item.text().split(",")[1].split(":")[1].strip()
                with get_db_connection() as conn:
                    with conn.cursor() as cursor:
                        # Email'e göre user_id'yi al
                        get_user_id_query = '''
                        SELECT user_id FROM school.user WHERE email = %s
                        '''
                        cursor.execute(get_user_id_query, (email,))
                        user_id = cursor.fetchone()

                        # User_id'yi kullanarak silme işlemini gerçekleştir
                        if user_id:
                            delete_query = '''
                            DELETE FROM school.user WHERE user_id = %s
                            '''
                            cursor.execute(delete_query, (user_id[0],))
                            # Remove the item from the list widget   
                            selected_row = self.findChild(QListWidget, "listWidget").row(selected_item)
                            self.findChild(QListWidget, "listWidget").takeItem(selected_row)      
                            # Success Message
                            QMessageBox.information(self, "Warning", "Teacher deleted successfully!")
                            #Add log file
                            logging.info(f"One teacher account rejected by {User._current_user.name}") 

            except Exception as e:
                print(f"Error getting teachers by status: {e}")
                # Extracting teacher email from the selected item's text
                
            
           
    def update_teacher_status(cls, email, new_status):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    sql_query = '''
                    UPDATE school.user
                    SET status = %s
                    WHERE email = %s AND user_type = 'teacher'
                    '''
                    cursor.execute(sql_query, (new_status, email))
                    conn.commit()

        except Exception as e:
            print(f"Error updating teacher status: {e}")
    #-----------------------------------------------------------------------------
          
    def display_announcement_to_delete(self):
        user = User._current_user
        announcements_to_delete = User.get_announcements_to_delete(user.email, user.user_type)
        self.announcement_to_delete_combobox = self.findChild(QtWidgets.QComboBox, "announcement_to_delete_combobox")
        self.announcement_to_delete_combobox.clear()
        self.announcement_to_delete_combobox.addItem("")
        for announcement in announcements_to_delete:
            self.announcement_to_delete_combobox.addItem(announcement['announcement'])

    def show_information(self):
        user = User._current_user
        self.teacher_profil_name_edit.setText(user.name)
        self.teahcer_profil_surname_edit.setText(user.surname)
        self.teacher_profil_birth_edit.setText(user.birthdate)
        self.teacher_profil_mail_edit.setText(user.email)
        self.teacher_profil_city_edit.setText(user.city)
        self.teacher_profil_tel_edit.setText(user.phone_number)

    def delete_announcement(self):
        self.announcement_to_delete_combobox = self.findChild(QtWidgets.QComboBox, "announcement_to_delete_combobox")
        announcement = self.announcement_to_delete_combobox.currentText()
        if announcement != "":
            User.delete_announcement(announcement)
            self.display_announcement_to_delete()
            self.announcement_to_delete_combobox.setCurrentIndex(0)

            # İndeks kontrolü yaparak hatanın önüne geç
            if self.current_announcement_index < len(User.get_announcements()):
                self.display_announcements(User.get_announcements()[self.current_announcement_index])
                self.showUpdateAlert(f"{announcement} is deleted!")
            else:
                # Eğer daha fazla anons yoksa, timer'ı durdur
                self.timer.stop()
                self.showUpdateAlert(f"{announcement} is deleted, no more announcements.")
        else:
            self.showUpdateAlert("Please select announcement to delete!")

       
            

    def create_announcement(self):
        ui_element = self.findChild(QtWidgets.QLineEdit, "announcement_lineEdit")
        text = ui_element.text()
        email = User._current_user.email
        if text != "":
            success, message = User.create_announcement(text, email)
            if success:
                self.display_announcements()  # announcement argümanını sağlamadan çağırın
                self.display_announcement_to_delete()
                self.showUpdateAlert(f"{message}")
                # Check the reference and clear the text
                check_ui_element = self.findChild(QtWidgets.QLineEdit, "announcement_lineEdit")
                if check_ui_element is not None:
                    check_ui_element.clear()
                else:
                    print("Reference to QLineEdit not found.")
            else:
                self.showUpdateAlert(f"{message}")
                
        else:
            self.showUpdateAlert(f"Announcement text cannot be empty!")
        
        
    def display_announcements(self,announcement=None):
        if announcement is None:
            # announcement belirtilmemişse, mevcut anonsları al
            announcements = User.get_announcements()

            if announcements is None or not announcements:
                print("No announcement found.")
                formatted_announcement = "No announcement"
            else:
                # Display the current announcement
                self.display_announcements(announcements[self.current_announcement_index])

                # Increment the counter for the next announcement
                self.current_announcement_index += 1

                # If there are more announcements, restart the timer for the next update
                if self.current_announcement_index < len(announcements):
                    self.timer.start(3000)
                else:
                    # All announcements displayed, stop the timer
                    self.timer.stop()
        else:
            # announcement belirtilmişse, sadece belirtilen anonsu göster
            if 'announcement' in announcement and 'user_id' in announcement and 'expiry_date' in announcement:
                formatted_announcement = (
                    f"<p style='font-size:14pt;'>{announcement['announcement']}</p>"
                    f"<p style='font-size:12pt; font-style:italic;'>Created by {announcement['user_id']} ({announcement['expiry_date']})</p>"
                )
                # Set the formatted text in the QTextBrowser
                ui_element = self.findChild(QtWidgets.QTextBrowser, "announcement_textbrowser")
                ui_element.setHtml(formatted_announcement)
            else:
                print("Invalid announcement format")
        
    def update_announcements(self):
        # Get announcements
        announcements = User.get_announcements()

        if announcements is None or not announcements:
            print("No announcement found.")
            formatted_announcement = "No announcement"
        else:
           #if User.get_announcements[{self.expiry_date}]>User.get_announcements[{self.expiry_date}]>:
           # Display the current announcement
                self.display_announcements(announcements[self.current_announcement_index])

            # Increment the counter for the next announcement
                self.current_announcement_index += 1

           # If there are more announcements, restart the timer for the next update
                if self.current_announcement_index < len(announcements):
                   self.timer.start(5000)
                else:
               # All announcements displayed, stop the timer
                   self.timer.stop()
    
    # def update_announcements(self):
    # # Get announcements
    #     announcements = User.get_announcements()

    #     if announcements is None or not announcements:
    #         print("No announcement found.")
    #         formatted_announcement = "No announcement"
    #     else:
    #         # Filter announcements based on expiry_date or creation_date if available
    #         current_time = datetime.now()
    #         filtered_announcements = []

    #         for announcement in announcements:
    #             if 'expiry_date' in announcement:
    #                 date_field = 'expiry_date'
    #             elif 'creation_date' in announcement:
    #                 date_field = 'creation_date'
    #             else:
    #                 print("Invalid announcement format - missing expiry_date or creation_date")
    #                 continue

    #             try:
    #                 announcement_date = datetime.fromisoformat(announcement[date_field])
    #             except ValueError:
    #                 print(f"Invalid date format for {date_field} in announcement.")
    #                 continue

    #             if announcement_date > current_time:
    #                 filtered_announcements.append(announcement)

    #         if not filtered_announcements:
    #             print("No active announcement found.")
    #             formatted_announcement = "No active announcement"
    #         else:
    #             # Display the current announcement
    #             self.display_announcements(filtered_announcements[self.current_announcement_index])

    #             # Increment the counter for the next announcement
    #             self.current_announcement_index += 1

    #             # If there are more announcements, restart the timer for the next update
    #             if self.current_announcement_index < len(filtered_announcements):
    #                 self.timer.start(5000)
    #             else:
    #                 # All announcements displayed, stop the timer
    #                 self.timer.stop()
    def open_create_lesson(self):

        self.open_create_lesson_window = CreateLesson(self.current_user_email)
        self.open_create_lesson_window.show()

    def open_create_mentor(self):

        self.open_create_mentor_window = CreateMentor(self.current_user_email)
        self.open_create_mentor_window.show()

    def show_lesson_attendance_page(self):

        self.open_lesson_attendance_window = LessonAttendance()
        self.open_lesson_attendance_window.show()

    def show_lesson_attendance_show(self):
        self.open_lesson_attendance_show = ShowAttLesson()
        self.open_lesson_attendance_show.show()

    def show_mentor_attendance_page(self):

        self.open_mentor_attendance_window = MentorAttendance()
        self.open_mentor_attendance_window.show()

    def show_mentor_attendance_show(self):
        self.open_mentor_attendance_show = ShowAttMentor()
        self.open_mentor_attendance_show.show()
    
    def refresh_lesson(self):

        teacher_plan_tab = self.findChild(QTableWidget, 'teacher_plan_lesson')
        table = User.get_LessonSchedule() 
       
        if isinstance(table, QTableWidget):
            teacher_plan_tab.clear()  

           
            teacher_plan_tab.setColumnCount(table.columnCount())
            teacher_plan_tab.setRowCount(table.rowCount())

            for i in range(table.rowCount()):
                for j in range(table.columnCount()):
                    item = table.item(i, j)
                    if item is not None:
                        teacher_plan_tab.setItem(i, j, QTableWidgetItem(item.text()))
            teacher_plan_tab.update()

    def refresh_mentor(self):

        teacher_plan_tab = self.findChild(QTableWidget, 'teacher_plan_mentoring')
        teacher_plan_tab.clearContents()
        self.show_Mentor_Schedule()   

    def create_task(self):
        self.task_name_input = self.findChild(QtWidgets.QLineEdit, 'task_name_input')
        self.due_date_input = self.findChild(QtWidgets.QDateEdit, 'due_date_input')

        task_name = self.task_name_input.text()
        due_date = self.due_date_input.date().toString("dd/MM/yyyy")
        assignees = self.selected_user_ids

        if task_name != "" and assignees != []:
            Task.create_task(User._current_user.user_id,task_name,due_date,assignees)
            print("Task is created", task_name, due_date, assignees)
            self.load_tasks()
            self.task_user_list.clearSelection()
            self.selected_user_ids = []
            self.task_name_input.setText("")
        else:
            self.showUpdateAlert(f"Task Name and Assignees cannot be empty")

    def show_user_list_for_task(self):
        self.task_user_list.setSelectionMode(QAbstractItemView.MultiSelection)
        users = User.get_emails_for_task_assign()

        for user_data in users:
            user_id, user_name, last_name, user_type, avatar_path = user_data

            # Create a QListWidgetItem and set the custom widget as its widget
            item = QListWidgetItem(self.task_user_list)
            user_item_widget = TeacherUserListItemWidget(user_id, user_name, last_name, user_type, avatar_path)
            item.setSizeHint(user_item_widget.sizeHint())

            self.task_user_list.addItem(item)
            self.task_user_list.setItemWidget(item, user_item_widget)

        self.task_user_list.setStyleSheet("""
            QListWidget::item {
                background-color: white;
            }
            QListWidget::item:selected {
                background-color: lightblue;
            }
            QListWidget::item:hover {
                background-color: lightgrey;
            }
        """)

    def load_tasks(self):
        tasks = Task.retrieve_task_per_creator(User._current_user.user_id)
        print(tasks)

        if tasks is None or not tasks:
            print("No tasks found.")
            return

        task_widget = self.findChild(QTableWidget, 'tasks_tableWidget')
        print("taskwidget created")
        task_widget.setRowCount(len(tasks))
        task_widget.setColumnCount(5)  # Reduced column count to 5

        # Define specific column widths
        column_widths = [200, 100, 250, 100, 100]  # Adjusted column widths

        headers = ["Task Name", "Due Date", "Assigned To", "Created By", "Created"]  # Removed "Status"
        task_widget.setHorizontalHeaderLabels(headers)

        # Set the combo box delegate for the "Status" column (column index 4)
        task_widget.setItemDelegateForColumn(3, ComboBoxDelegate())  # Adjusted column index

        # Set specific column widths
        for col, width in enumerate(column_widths):
            task_widget.setColumnWidth(col, width)

        # Set total table width based on column widths
        total_width = sum(column_widths)
        task_widget.setMinimumWidth(total_width)
        task_widget.setMaximumWidth(total_width+30)

        

        # Populate the table
        for row, task_info in enumerate(tasks):
            task_id, task_name, due_date, created_at, user_info_list = task_info

            task_widget.setItem(row, 0, QTableWidgetItem(task_name))
            task_widget.item(row, 0).setData(Qt.UserRole, task_id)

            #selected_row = task_widget.currentRow()
            #task_id = task_widget.item(selected_row, 0).data(Qt.UserRole)

            task_widget.setItem(row, 1, QTableWidgetItem(due_date))

            # Create a widget for the "Assigned To" column
            assigned_to_widget = QWidget()
            assigned_to_layout = QVBoxLayout(assigned_to_widget)

            # Assuming the user_info field is a list with user information
            for user_info in user_info_list:
                # Create a horizontal layout for each user
                user_layout = QHBoxLayout()

                # Create a QLabel for the avatar
                avatar_label = QLabel()
                avatar_path = user_info.get('avatar', 'default_avatar.png')
                avatar_pixmap = QPixmap(avatar_path).scaledToWidth(30).scaledToHeight(30, Qt.SmoothTransformation)

                # Create a circular mask
                mask = QBitmap(avatar_pixmap.size())
                mask.fill(Qt.color0)
                painter = QPainter(mask)
                painter.setBrush(Qt.color1)
                painter.drawEllipse(0, 0, mask.width(), mask.height())
                painter.end()

                # Apply the circular mask to the avatar
                avatar_pixmap.setMask(mask)

                avatar_label.setPixmap(avatar_pixmap)
                user_layout.addWidget(avatar_label)

                # Create a QLabel for user name and surname
                name_label = QLabel(f"{user_info['name']} {user_info['last_name']}")
                user_layout.addWidget(name_label)

                # Create a QLabel for status
                status_label = QLabel(user_info['status'].upper())
                font = status_label.font()
                font.setBold(True)
                status_label.setFont(font)
                user_layout.addWidget(status_label)

                # Add the user layout to the assigned_to_layout
                assigned_to_layout.addLayout(user_layout)

            #headers = ["Task Name", "Due Date", "Assigned To", "Created By", "Created"]  # Removed "Status"
            # Set the layout for the "Assigned To" column
            task_widget.setCellWidget(row, 2, assigned_to_widget)

            task_widget.setItem(row, 3, QTableWidgetItem(User._current_user.name))  # Replace with actual creator information

            # Create a QTableWidgetItem for the "Status" column
            #status_item = QTableWidgetItem("N/A")  # Replace with actual status information
            #status_item.setData(Qt.UserRole, task_id)  # Assuming you want to store task_id as user data

            #task_widget.setItem(row, 4, status_item)
            task_widget.setItem(row, 4,QTableWidgetItem(created_at))# Replace with actual created information

            # Adjust row height based on the number of users
            row_height = len(user_info_list) * 60
            task_widget.setRowHeight(row, row_height)


    def on_item_double_clicked(self, item):
        # Prevent editing for certain columns
        if item.column() in [0,2, 3, 5]:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Clear the editable flag
        else:
            item.setFlags(item.flags() | Qt.ItemIsEditable)  # Set the editable flag

    def on_item_changed(self, item):
        row = item.row()
        col = item.column()
        # print(item.row(), item.column())
        if item.tableWidget().item(row, 2) is not None:
            task_name_ilk = item.tableWidget().item(row, 0).text()
            assigned_to_email = item.tableWidget().item(row, 2).text()
            new_value = item.text()
            print("new value: ", new_value)

            if 1 == 0:  # Task Name column
                if Task.update_task_teacher(task_name_ilk, assigned_to_email, task_name=new_value):
                    self.showUpdateAlert(f"Task name is updated to {new_value}")
                else:
                    print("Task not updated.")
            elif col == 1:  # Due Date column
                if Task.update_task_teacher(task_name_ilk, assigned_to_email, due_date=new_value):
                    self.showUpdateAlert(f"Due date is updated to {new_value}")
                else:
                    print("Task not updated.")
            elif col == 4:  # Status column
                if Task.update_task_teacher(task_name_ilk, assigned_to_email, status=new_value):
                    self.showUpdateAlert(f"Status is updated to {new_value}")
                else:
                    print("Task not updated.")
            else:
                # Handle the case where the item was not edited
                print("Item not edited.")
        else:
            print("Item is None.")
    
    def showUpdateAlert(self, alert):
        message = alert
        QMessageBox.information(None, "Item Updated", message, QMessageBox.Ok)

    def show_Lesson_Schedule(self):

        teacher_plan_tab = self.findChild(QTableWidget, 'teacher_plan_lesson')
        table = User.get_LessonSchedule()
        layout = QVBoxLayout()
        layout.addWidget(table)        
        teacher_plan_tab.setLayout(layout)
      

    def show_Mentor_Schedule(self):

        teacher_plan_tab = self.findChild(QTableWidget, 'teacher_plan_mentoring')    
        table = User.get_Mentor_Schedule()
        layout = QVBoxLayout()
        layout.addWidget(table)        
        teacher_plan_tab.setLayout(layout)
  
    def show_Lesson_Attendance(self):

        teacher_lesson_attendance = self.findChild(QTableView, 'teacher_attendance_lesson')
        table = User.get_Lesson_Attendance()
        layout = QVBoxLayout()
        layout.addWidget(table)
        teacher_lesson_attendance.setLayout(layout)

    def show_Mentor_Attendance(self):

        teacher_mentor_attendance = self.findChild(QTableView, 'teacher_attendance_mentor')
        table = User.get_Mentor_Attendance()
        layout = QVBoxLayout()
        layout.addWidget(table)        
        teacher_mentor_attendance.setLayout(layout)

class ComboBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.column() == 4:
            combo_box = QComboBox(parent)
            combo_box.addItems(["Open", "In Progress", "Completed"])
            return combo_box
        return None

    def setEditorData(self, editor, index):
        value = index.model().data(index, role=Qt.DisplayRole)
        editor.setCurrentText(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Read the style sheet from lightstyle.qss
    style_sheet = Path("lightstyle.qss").read_text()
    app.setStyleSheet(style_sheet)

    app_window = Teacher_Main_Window()
    app_window.show()

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(app_window)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

