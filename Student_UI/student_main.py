
import sys, os
sys.path.append(os.getcwd())
from pathlib import Path

from Classes.user import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from Student_UI.Ui_Student_Ui import *
from Classes.task import Task
from Classes.user import User
from Student_UI.LessonAttendance import *
from Student_UI.MentorAttendance import *
from sign.Ui_login_screen import Ui_Form as Ui_MainWindow_3

class UserListItemWidget(QWidget):
    def __init__(self, user_id, user_name, last_name, user_type, avatar_path):
        super(UserListItemWidget, self).__init__()

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
        self.tasks_tableWidget.setStyleSheet("background-color: transparent;")

        


class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_Window,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Student Page")

        User.set_currentuser("student@example.com")


        current_date_time = QDateTime.currentDateTime()
        formatted_date = current_date_time.toString("dd-MM-yyyy")
        self.student_main_name.setText(f"Welcome {User._current_user.name}")
        self.student_main_date.setText(f"{formatted_date}")
        
        tab_widget = self.tabWidget
        tab_widget.removeTab(5)
        tab_widget.removeTab(4)

        self.load_student_tasks()
        #self.load_tasks(User._current_user.email)
        self.show_Lesson_Schedule()
        self.show_Mentor_Schedule()


        self.display_announcements()
        self.lesson_attendance.clicked.connect(self.show_lesson_attendance_page)
        self.mentor_attendance.clicked.connect(self.show_mentor_attendance_page)
        self.show_information()

        self.update_information_Button.clicked.connect(self.update_information)

        #self.sign_out_button.clicked.connect(self.open_login)

        self.tabWidget.setCurrentIndex(0)
        self.selected_task_ids = []
        self.tasks_tableWidget.setStyleSheet("") 
        status_options_list = ["Select a Status", "Assigned", "In Progress", "Completed"]
        self.status_options.addItems(status_options_list)
        self.update_status_button.clicked.connect(self.update_task_status)
        

    def update_task_status(self):
        if self.status_options.currentText() == "Select a Status":
            self.showUpdateAlert("Please select a status first")
        elif self.selected_task_ids == []:
            self.showUpdateAlert("Please select a task to update status")
        else:
            Task.update_task_status(User._current_user.user_id,self.selected_task_ids,self.status_options.currentText())
            print("Tasks are updated", self.selected_task_ids, self.status_options.currentText())
            self.status_options.setCurrentIndex(0)
            self.load_student_tasks()
            self.showUpdateAlert("Statuses for selected tasks are updated")


    def update_assigned_to_background(self, selected_rows):
        task_widget = self.findChild(QTableWidget, 'tasks_tableWidget')

        for row in range(task_widget.rowCount()):
            assigned_to_widget = task_widget.cellWidget(row, 3)

            if assigned_to_widget:
                background_color = (
                    QColor(255, 255, 255)  # Set your desired background color
                    if task_widget.item(row, 0).data(Qt.UserRole) in selected_rows
                    else QColor(0, 0, 0, 0)  # Transparent background if not selected
                )

                assigned_to_widget.setStyleSheet(f"background-color: transparent;")

    def on_item_selection_changed(self):
        selected_rows = [row.row() for row in self.tasks_tableWidget.selectionModel().selectedRows()]
        self.selected_task_ids = [self.tasks_tableWidget.item(row, 0).data(Qt.UserRole) for row in selected_rows]

        # Update background color of the "Assigned To" column
        self.update_assigned_to_background(self.selected_task_ids)

        # Print or use the selected_task_ids as needed
        print("Selected Task IDs:", self.selected_task_ids)

    

    def load_student_tasks(self):
        
        tasks = Task.retrieve_student_tasks(User._current_user.user_id)
        print(tasks)

        if tasks is None or not tasks:
            print("No tasks found.")
            return

        task_widget = self.findChild(QTableWidget, 'tasks_tableWidget')
        task_widget.clear()
        task_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        task_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        task_widget.itemSelectionChanged.connect(self.on_item_selection_changed)


        print("taskwidget created")
        task_widget.setRowCount(len(tasks))
        task_widget.setColumnCount(5)  # Adjusted column count to 6

        # Define specific column widths
        column_widths = [200, 100, 100, 250, 100]  # Adjusted column widths

        headers = ["Task Name", "Status", "Due Date", "Created By", "Created"]
        task_widget.setHorizontalHeaderLabels(headers)

        # Set specific column widths
        for col, width in enumerate(column_widths):
            task_widget.setColumnWidth(col, width)

        # Set total table width based on column widths
        total_width = sum(column_widths)
        task_widget.setMinimumWidth(total_width)
        task_widget.setMaximumWidth(total_width + 30)

        # Populate the table
        for row, task_info in enumerate(tasks):
            task_id, user_id, status, task_name, due_date, created_at, created_by, name, last_name, avatar_path = task_info


            task_widget.setItem(row, 0, QTableWidgetItem(task_name))
            task_widget.item(row, 0).setData(Qt.UserRole, task_id)

            # Create a QTableWidgetItem for the "Status" column
            status_item = QTableWidgetItem(status)
            status_item.setData(Qt.UserRole, task_id)
            task_widget.setItem(row, 1, status_item)

            task_widget.setItem(row, 2, QTableWidgetItem(due_date))

            # Create a widget for the "Assigned To" column
            assigned_to_widget = QWidget()
            assigned_to_layout = QVBoxLayout(assigned_to_widget)

            # Create a horizontal layout for the user
            user_layout = QHBoxLayout()

            # Create a QLabel for the avatar
            avatar_label = QLabel()
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
            name_label = QLabel(f"{name} {last_name}")
            user_layout.addWidget(name_label)

            # Add the user layout to the assigned_to_layout
            assigned_to_layout.addLayout(user_layout)

            # Set the layout for the "Assigned To" column
            task_widget.setCellWidget(row, 3, assigned_to_widget)

            task_widget.setItem(row, 4, QTableWidgetItem(created_at))

            # Adjust row height
            task_widget.setRowHeight(row, 60)

        style_sheet = """
            QTableWidget {
                background-color: #ffffff;  /* Set your desired background color for unselected rows */
                color: black;  /* Set the text color for unselected rows */
            }
            QTableWidget::item:selected {
                background-color: #a6c9e2;  /* Set your desired background color for selected rows */
                color: black;  /* Set the text color for selected rows */
            }
            QTableWidget::item:selected:!active {
                background-color: #a6c9e2;  /* Set your desired background color for selected rows when not active */
                color: black;  /* Set the text color for selected rows when not active */
            }
            QTableWidget::item:alternate {
                background-color: #f5f5f5;  /* Set your desired background color for alternate rows */
                color: black;  /* Set the text color for alternate rows */
            }
        """
        self.tasks_tableWidget.setStyleSheet(style_sheet)

    def checkbox_changed(self, state, task_id):
        if state == Qt.Checked:
            self.selected_task_ids.append(task_id)
        else:
            self.selected_task_ids.remove(task_id)

    def open_login(self):
        self.ui_main_3_window = QtWidgets.QMainWindow()
        self.ui_main_3 = Ui_MainWindow_3()
        self.ui_main_3.setupUi(self.ui_main_3_window)
        #self.ui_main_3_window.setStyleSheet(Path("lightstyle.qss").read_text())
        self.ui_main_3_window.show()
        self.ui_main_3_window.resize(440,400)
        self.ui_main_3.enter_Button.clicked.connect(Ui_MainWindow_3.check_enter) 


    def update_information(self):
        self.student_profil_tel_edit = self.findChild(QtWidgets.QTextEdit,"student_profil_tel_edit")
        self.student_profil_city_edit = self.findChild(QtWidgets.QTextEdit,"student_profil_city_edit")

        new_tel = self.student_profil_tel_edit.toPlainText()
        new_city = self.student_profil_city_edit.toPlainText()
        updated_info = {"phone_number": new_tel, "city": new_city  }
        User.update_user_information(User._current_user.email, **updated_info)
        self.showUpdateAlert("Information is updated")

    def show_information(self):
        user = User._current_user
        self.student_profil_name_edit.setText(user.name)
        self.student_profil_surname_edit.setText(user.surname)
        self.student_profil_birth_edit.setText(user.birthdate)
        self.student_profil_mail_edit.setText(user.email)
        self.student_profil_city_edit.setText(user.city)
        self.student_profil_tel_edit.setText(user.phone_number)


    def display_announcements(self):
        # Get announcements
        announcements = User.get_announcements()

        if announcements is None or not announcements:
            print("No announcement found.")
            formatted_announcements = "No announcement"
        else:
            # Format announcements with gaps
            formatted_announcements = "<hr>".join(
        f"<p style='font-size:14pt;'>{announcement['announcement']}</p>"
        f"<p style='font-size:12pt; font-style:italic;'>Announcement by {announcement['created_by']} ({announcement['timestamp']})</p>"
        for announcement in announcements
    )
        # Set the formatted text in the QTextBrowser
        ui_element= self.findChild(QtWidgets.QTextBrowser, "announcements_textBrowser")
        ui_element.setHtml(formatted_announcements)
        #self.announcements_textBrowser.setHtml(formatted_announcements)



    def show_Lesson_Schedule(self):

        student_plan_tab = self.findChild(QTableWidget, 'student_plan_lesson_list')
        table = User.get_LessonSchedule()
        layout = QVBoxLayout()
        layout.addWidget(table)        
        student_plan_tab.setLayout(layout)
      

    def show_Mentor_Schedule(self):

        student_plan_tab = self.findChild(QTableWidget, 'student_plan_mentor_list')    
        table = User.get_Mentor_Schedule()
        layout = QVBoxLayout()
        layout.addWidget(table)        
        student_plan_tab.setLayout(layout)
    
    def showUpdateAlert(self, alert):
        message = alert
        QMessageBox.information(None, "Item Updated", message, QMessageBox.Ok)

    def show_lesson_attendance_page(self):

        self.open_lesson_attendance_window = LessonAttendance(User._current_user.email)
        self.open_lesson_attendance_window.show()

    def show_mentor_attendance_page(self):

        self.open_lesson_attendance_show = MentorAttendance(User._current_user.email)
        self.open_lesson_attendance_show.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(Path("lightstyle.qss").read_text())
    app_window = Main_Window()    
    #app_window.setStyleSheet(Path("lightstyle.qss").read_text())
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(app_window) 
    widget.setStyleSheet(Path("lightstyle.qss").read_text())
    widget.show()
    try:
        sys.exit(app.exec_())

    except:
        print("Exiting")


