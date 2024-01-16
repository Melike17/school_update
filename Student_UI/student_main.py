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


class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_Window,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Student Page")

        #User.set_currentuser("student@example.com")


        current_date_time = QDateTime.currentDateTime()
        formatted_date = current_date_time.toString("dd-MM-yyyy")
        self.student_main_name.setText(f"Welcome {User._current_user.name}")
        self.student_main_date.setText(f"{formatted_date}")
        
        tab_widget = self.tabWidget
        tab_widget.removeTab(5)
        tab_widget.removeTab(4)

        self.load_tasks(User._current_user.email)
        self.show_Lesson_Schedule()
        self.show_Mentor_Schedule()


        self.display_announcements()
        self.lesson_attendance.clicked.connect(self.show_lesson_attendance_page)
        self.mentor_attendance.clicked.connect(self.show_mentor_attendance_page)
        self.show_information()

        self.update_information_Button.clicked.connect(self.update_information)

        #self.sign_out_button.clicked.connect(self.open_login)

        self.tabWidget.setCurrentIndex(0)

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

    def load_tasks(self, email):
        tasks = Task.retrieve_task_per_assignee(email)
        print(tasks)

        if tasks is None or not tasks:
            print("No tasks found.")
            return

        table_widget = self.findChild(QTableWidget, 'tasks_tableWidget')
        table_widget.setRowCount(len(tasks))
        table_widget.setColumnCount(6)

        headers = ["Task Name", "Due Date", "Assigned To", "Created By", "Status", "Created"]
        table_widget.setHorizontalHeaderLabels(headers)
        
        # Set the combo box delegate for the "Status" column (column index 4)
        table_widget.setItemDelegateForColumn(4, ComboBoxDelegate())

        # Populate the table
        for row, task in enumerate(tasks):
            table_widget.setItem(row, 0, QTableWidgetItem(task.task_name))
            table_widget.setItem(row, 1, QTableWidgetItem(task.due_date))
            table_widget.setItem(row, 2, QTableWidgetItem(task.assigned_to_email))
            table_widget.setItem(row, 3, QTableWidgetItem(task.created_by))
            
            # Create a QTableWidgetItem for the "Status" column
            status_item = QTableWidgetItem(task.status)
            status_item.setData(Qt.UserRole, task)

            table_widget.setItem(row, 4, status_item)
            table_widget.setItem(row, 5, QTableWidgetItem(task.created))

        # Connect the itemDoubleClicked signal to a slot
        table_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

    def on_item_double_clicked(self, item):
        # Prevent editing for certain columns
        if item.column() in [0, 1, 2, 3, 5]:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Clear the editable flag
        else:
            item.setFlags(item.flags() | Qt.ItemIsEditable)  # Set the editable flag

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

    def setModelData(self, editor, model, index):
        if index.column() == 4:
            value = editor.currentText()
            model.setData(index, value, role=Qt.EditRole)

            row = index.row()
            task_name = model.data(model.index(row, 0), role=Qt.DisplayRole)
            created_by = model.data(model.index(row, 3), role=Qt.DisplayRole)
            new_status = editor.currentText()

            Task.update_task_status(task_name, created_by, new_status)

            # Show an alert
            self.showUpdateAlert(task_name, new_status)

    def showUpdateAlert(self, task_name, new_status):
        message = f"Task:  {task_name} status is updated to: {new_status}"
        QMessageBox.information(None, "Item Updated", message, QMessageBox.Ok)



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









