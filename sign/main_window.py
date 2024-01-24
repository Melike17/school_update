<<<<<<< HEAD
import sys, os

sys.path.append(os.getcwd())

import re
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from sign.Ui_main_2 import Ui_MainWindow as Ui_MainWindow_2
from sign.Ui_login_screen import Ui_Form as Ui_MainWindow_3
from sign.Ui_signup_screen import Ui_Form as Ui_MainWindow_4
from Classes.user import User
from Student_UI.student_main import Main_Window as Ui_MainWindow_5
from Teacher_UI.teacher_main import Main_Window as Ui_MainWindow_6

class Main_Window(QMainWindow, Ui_MainWindow_2):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.resize(640,480)       
        self.setWindowTitle("School Info")
        self.login_Button.clicked.connect(self.open_login)
        self.login_Button.clicked.connect(self.close)
        self.signup_Button.clicked.connect(self.open_signup)
        self.signup_Button.clicked.connect(self.close)
       
        
    
    def create_Student(self,name, surname, email, birthday, city,phone_number, password,status, avatar_path):
        if not (User.email_exists(email)):
            User.create_user(name, surname, email, birthday, city, phone_number, password, user_type="student",status=status,avatar_path=avatar_path)
            print("User created successfully.")
            # Close this window after saving the user
            self.ui_main_3_window.close()
            # Open the login screen
            self.open_login()
        else:
            QMessageBox.warning(None, 'Warning', f'The email {email} already exists.', QMessageBox.Ok)
        
    def create_Teacher(self,name, surname, email, birthday, city,phone_number, password,status, avatar_path):
        if not User.email_exists(email):
            User.create_user(name, surname, email, birthday, city, phone_number, password, user_type="teacher",status=status, avatar_path=avatar_path)
            QMessageBox.warning(None, 'Warning', 'Please wait for admin to confirm!', QMessageBox.Ok)
            self.ui_main_3_window.close()
            # Open the login screen
            self.open_login()
        else:
            QMessageBox.warning(None, 'Warning', f'The email {email} already exists.', QMessageBox.Ok)
            
    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email)
    
    def is_valid_password(self,password):
        password = self.ui_main_3.password.text()

        if len(password) <= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password) and any(c.isascii() and not c.isalnum() for c in password):
            return True
        else:
            return False
    def is_equal_password(self,password,repassword):
        password = self.ui_main_3.password.text()
        repassword= self.ui_main_3.repassword.text()
        if password == repassword:
            return True
        else:
            return False
        
    def check_enter(self):
        email = self.ui_main_3.email.text()
        password = self.ui_main_3.password.text()
        if (email == '' or password == ''):
            QMessageBox.warning(None, 'Warning', f'Please fill in the blanks!', QMessageBox.Ok)
            #self.ui_main_3_window.statusBar().showMessage("Please fill in the blanks!", 2000)
        elif not self.is_valid_email(email):
            QMessageBox.warning(None, 'Warning', f'Please enter a valid email address!', QMessageBox.Ok)
            #self.ui_main_3_window.statusBar().showMessage("Please enter a valid email address!", 2000)
        elif not self.is_valid_password(password):
            QMessageBox.warning(None, 'Warning', f'Please enter a valid password!', QMessageBox.Ok)
            #self.ui_main_3_window.statusBar().showMessage("Please enter a valid password!", 2000)
        else:
            user_data = User.login(email, password)
            if user_data:
                # successful enter for users
                user_type = user_data.get('user_type')
                User.set_currentuser(email)
                self.open_main_window(user_type)
                
            else:
                QMessageBox.warning(None, 'Warning', f'Invalid email or password!', QMessageBox.Ok)
                #self.ui_main_3_window.statusBar().showMessage("Invalid email or password!", 2000

    def open_main_window(self, user_type):
        if user_type == 'admin':
            # Open Admin account in Teacher UI
            
            self.ui_main_3_window = QtWidgets.QMainWindow()
            self.ui_main_3 = Ui_MainWindow_6()
            self.ui_main_3.setupUi(self.ui_main_3_window)
            self.ui_main_3.show()
            self.ui_main_3_window.resize(440,400)
        elif user_type == 'teacher':
            print("Opening teacher window with status:", User._current_user.status) 
            if  User._current_user.status =='active':
                self.ui_main_3_window = QtWidgets.QMainWindow()
                self.ui_main_3 = Ui_MainWindow_6()
                self.ui_main_3.setupUi(self.ui_main_3_window)
                self.ui_main_3.show()
                self.ui_main_3_window.resize(440,400)
            
        elif user_type == 'student':
            self.ui_main_3_window = QtWidgets.QMainWindow()
            self.ui_main_3 = Ui_MainWindow_5()
            self.ui_main_3.setupUi(self.ui_main_3_window)
            self.ui_main_3.show()
            self.ui_main_3_window.resize(440,400)
        else:
            print("Unknown user type!")
        

            
    def check_enter_signup(self):
        name = self.ui_main_3.name.text()
        surname = self.ui_main_3.surname.text()
        birthday = self.ui_main_3.birthday.date().toString(QtCore.Qt.ISODate) #ISO standart for Date
        city = self.ui_main_3.city.text()
        email = self.ui_main_3.email.text()
        phone_number=self.ui_main_3.phone_number.text()
        password = self.ui_main_3.password.text()
        repassword = self.ui_main_3.repassword.text()
        student_checked = self.ui_main_3.student_radioButton.isChecked()
        teacher_checked = self.ui_main_3.teacher_radioButton.isChecked()
        
        
        if not all([name, surname, birthday, city, email, phone_number, password, repassword]):
            QMessageBox.warning(None, 'Warning', 'Please fill in all the fields!', QMessageBox.Ok)
        elif not self.is_valid_email(email):
            QMessageBox.warning(None, 'Warning', 'Please enter a valid email address!', QMessageBox.Ok)
        elif not self.is_valid_password(password):
            QMessageBox.warning(None, 'Warning', 'Please enter a valid password!', QMessageBox.Ok)
        elif not self.is_equal_password(password, repassword):
            QMessageBox.warning(None, 'Warning', 'Passwords do not match. Please check your password!', QMessageBox.Ok)
        elif student_checked:
            
            self.create_Student(name, surname, email, birthday, city, phone_number, password,status='active', avatar_path='./assets/login.png')
        elif teacher_checked:
            
            self.create_Teacher(name, surname, email, birthday, city, phone_number, password,status='passive', avatar_path='./assets/login.png')
            
        else:
            QMessageBox.warning(None, 'Warning', 'Please select a role!', QMessageBox.Ok)

    def open_login(self):
        self.ui_main_3_window = QtWidgets.QMainWindow()
        self.ui_main_3 = Ui_MainWindow_3()
        self.ui_main_3.setupUi(self.ui_main_3_window)
        #self.ui_main_3_window.setStyleSheet(Path("lightstyle.qss").read_text())
        self.ui_main_3_window.show()
        self.ui_main_3_window.resize(440,400)
        self.ui_main_3.enter_Button.clicked.connect(self.check_enter) 
        
            
    def open_signup(self):
        self.ui_main_3_window = QtWidgets.QMainWindow()
        self.ui_main_3 = Ui_MainWindow_4()
        self.ui_main_3.setupUi(self.ui_main_3_window)
        #self.ui_main_3_window.setStyleSheet(Path("lightstyle.qss").read_text())
        self.ui_main_3_window.show()
        self.ui_main_3_window.resize(440,400)
        self.ui_main_3.sign_Button.clicked.connect(self.check_enter_signup)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_window = Main_Window()
    #app_window.setStyleSheet(Path("lightstyle.qss").read_text())
    app_window.show()
    sys.exit(app.exec_())

=======
import sys, os
import logging
sys.path.append(os.getcwd())
import hashlib
import re
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from sign.Ui_main_2 import Ui_MainWindow as Ui_MainWindow_2
from sign.Ui_login_screen import Ui_Form as Ui_MainWindow_3
from sign.Ui_signup_screen import Ui_Form as Ui_MainWindow_4
from Classes.user import User
from Student_UI.student_main import Main_Window as Ui_MainWindow_5
from Teacher_UI.teacher_main import Main_Window as Ui_MainWindow_6

class Main_Window(QMainWindow, Ui_MainWindow_2):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.resize(640,480)       
        self.setWindowTitle("School Info")
        self.login_Button.clicked.connect(self.open_login)
        self.login_Button.clicked.connect(self.close)
        self.signup_Button.clicked.connect(self.open_signup)
        self.signup_Button.clicked.connect(self.close)
       
        
    def hash_password(self, password):
        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    def create_Student(self,name, surname, email, birthday, city,phone_number, password,status, avatar_path):
        if not (User.email_exists(email)):
            User.create_user(name, surname, email, birthday, city, phone_number, password, user_type="student",status=status,avatar_path=avatar_path)
            print("User created successfully.")
            #Add log file
            logging.info(f"Student created successfully by {name}: {email}")
            # Close this window after saving the user
            self.ui_main_3_window.close()
            # Open the login screen
            self.open_login()
        else:
            QMessageBox.warning(None, 'Warning', f'The email {email} already exists.', QMessageBox.Ok)
        
    def create_Teacher(self,name, surname, email, birthday, city,phone_number, password,status, avatar_path):
        if not User.email_exists(email):
            User.create_user(name, surname, email, birthday, city, phone_number, password, user_type="teacher",status=status, avatar_path=avatar_path)
            QMessageBox.warning(None, 'Warning', 'Please wait for admin to confirm!', QMessageBox.Ok)
            #Add log file
            logging.info(f"Teacher created successfully by {name}: {email}")
            self.ui_main_3_window.close()
            # Open the login screen
            self.open_login()
        else:
            QMessageBox.warning(None, 'Warning', f'The email {email} already exists.', QMessageBox.Ok)
            
    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email)
    
    def is_valid_password(self,password):
        password = self.ui_main_3.password.text()

        if len(password) <= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password) and any(c.isascii() and not c.isalnum() for c in password):
            return True
        else:
            return False
    def is_equal_password(self,password,repassword):
        password = self.ui_main_3.password.text()
        repassword= self.ui_main_3.repassword.text()
        if password == repassword:
            return True
        else:
            return False
        
    def check_enter(self):
        email = self.ui_main_3.email.text()
        password = self.ui_main_3.password.text()
        # Şifreyi hash'leme
        hashed_password = self.hash_password(password)
        password=hashed_password
        if (email == '' or password == ''):
            QMessageBox.warning(None, 'Warning', f'Please fill in the blanks!', QMessageBox.Ok)
            #self.ui_main_3_window.statusBar().showMessage("Please fill in the blanks!", 2000)
        elif not self.is_valid_email(email):
            QMessageBox.warning(None, 'Warning', f'Please enter a valid email address!', QMessageBox.Ok)
            #self.ui_main_3_window.statusBar().showMessage("Please enter a valid email address!", 2000)
        elif not self.is_valid_password(password):
            QMessageBox.warning(None, 'Warning', f'Please enter a valid password!', QMessageBox.Ok)
            #self.ui_main_3_window.statusBar().showMessage("Please enter a valid password!", 2000)
        else:
            user_data = User.login(email, password)
            if user_data:
                # successful enter for users
                user_type = user_data.get('user_type')
                User.set_currentuser(email)
                self.open_main_window(user_type)
                
            else:
                QMessageBox.warning(None, 'Warning', f'Invalid email or password!', QMessageBox.Ok)
                #self.ui_main_3_window.statusBar().showMessage("Invalid email or password!", 2000

    def open_main_window(self, user_type):
        if user_type == 'admin':
            # Open Admin account in Teacher UI
            #Add log file
            logging.info(f"Admin login successfully")
            self.ui_main_3_window = QtWidgets.QMainWindow()
            self.ui_main_3 = Ui_MainWindow_6()
            self.ui_main_3.setupUi(self.ui_main_3_window)
            self.ui_main_3.show()
            self.ui_main_3_window.resize(440,400)
        elif user_type == 'teacher':
            print("Opening teacher window with status:", User._current_user.status) 
            if  User._current_user.status =='active':
                #Add log file
                logging.info(f"{User._current_user.name} login successfully ")
                self.ui_main_3_window = QtWidgets.QMainWindow()
                self.ui_main_3 = Ui_MainWindow_6()
                self.ui_main_3.setupUi(self.ui_main_3_window)
                self.ui_main_3.show()
                self.ui_main_3_window.resize(440,400)
            
        elif user_type == 'student':
            #Add log file
            logging.info(f"{User._current_user.name} login successfully ")
            self.ui_main_3_window = QtWidgets.QMainWindow()
            self.ui_main_3 = Ui_MainWindow_5()
            self.ui_main_3.setupUi(self.ui_main_3_window)
            self.ui_main_3.show()
            self.ui_main_3_window.resize(440,400)
        else:
            print("Unknown user type!")
        

            
    def check_enter_signup(self):
        name = self.ui_main_3.name.text()
        surname = self.ui_main_3.surname.text()
        birthday = self.ui_main_3.birthday.date().toString(QtCore.Qt.ISODate) #ISO standart for Date
        city = self.ui_main_3.city.text()
        email = self.ui_main_3.email.text()
        phone_number=self.ui_main_3.phone_number.text()
        password = self.ui_main_3.password.text()
        repassword = self.ui_main_3.repassword.text()
        student_checked = self.ui_main_3.student_radioButton.isChecked()
        teacher_checked = self.ui_main_3.teacher_radioButton.isChecked()
        
        
        
        
        if not all([name, surname, birthday, city, email, phone_number, password, repassword]):
            QMessageBox.warning(None, 'Warning', 'Please fill in all the fields!', QMessageBox.Ok)
        elif not self.is_valid_email(email):
            QMessageBox.warning(None, 'Warning', 'Please enter a valid email address!', QMessageBox.Ok)
        elif not self.is_valid_password(password):
            QMessageBox.warning(None, 'Warning', 'Please enter a valid password!', QMessageBox.Ok)
        elif not self.is_equal_password(password, repassword):
            QMessageBox.warning(None, 'Warning', 'Passwords do not match. Please check your password!', QMessageBox.Ok)
        elif student_checked:
            # Password to hash'leme
            hashed_password = self.hash_password(password)
            password= hashed_password
            self.create_Student(name, surname, email, birthday, city, phone_number, password,status='active', avatar_path='./assets/login.png')
        elif teacher_checked:
            # Password to hash'leme
            hashed_password = self.hash_password(password)
            password= hashed_password
            self.create_Teacher(name, surname, email, birthday, city, phone_number, password,status='passive', avatar_path='./assets/login.png')
            
        else:
            QMessageBox.warning(None, 'Warning', 'Please select a role!', QMessageBox.Ok)

    def open_login(self):
        self.ui_main_3_window = QtWidgets.QMainWindow()
        self.ui_main_3 = Ui_MainWindow_3()
        self.ui_main_3.setupUi(self.ui_main_3_window)
        #self.ui_main_3_window.setStyleSheet(Path("lightstyle.qss").read_text())
        self.ui_main_3_window.show()
        self.ui_main_3_window.resize(440,400)
        self.ui_main_3.enter_Button.clicked.connect(self.check_enter) 
        
            
    def open_signup(self):
        self.ui_main_3_window = QtWidgets.QMainWindow()
        self.ui_main_3 = Ui_MainWindow_4()
        self.ui_main_3.setupUi(self.ui_main_3_window)
        #self.ui_main_3_window.setStyleSheet(Path("lightstyle.qss").read_text())
        self.ui_main_3_window.show()
        self.ui_main_3_window.resize(440,400)
        self.ui_main_3.sign_Button.clicked.connect(self.check_enter_signup)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_window = Main_Window()
    #app_window.setStyleSheet(Path("lightstyle.qss").read_text())
    app_window.show()
    sys.exit(app.exec_())

>>>>>>> main
