# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\MainUser\Documents\GitHub\Sema\school_update\sign\signup_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 800)
        Form.setMinimumSize(QtCore.QSize(500, 800))
        Form.setMaximumSize(QtCore.QSize(500, 800))
        Form.setStyleSheet("background-color: rgb(57, 57, 57);\n"
"")
        self.name = QtWidgets.QLineEdit(Form)
        self.name.setGeometry(QtCore.QRect(100, 160, 300, 30))
        self.name.setMinimumSize(QtCore.QSize(300, 30))
        self.name.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.name.setFont(font)
        self.name.setStyleSheet("\n"
"background-color: rgb(255, 255, 255);")
        self.name.setObjectName("name")
        self.surname = QtWidgets.QLineEdit(Form)
        self.surname.setGeometry(QtCore.QRect(100, 220, 300, 30))
        self.surname.setMinimumSize(QtCore.QSize(300, 30))
        self.surname.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.surname.setFont(font)
        self.surname.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.surname.setObjectName("surname")
        self.city = QtWidgets.QLineEdit(Form)
        self.city.setGeometry(QtCore.QRect(100, 400, 300, 30))
        self.city.setMinimumSize(QtCore.QSize(300, 30))
        self.city.setMaximumSize(QtCore.QSize(300, 30))
        self.city.setSizeIncrement(QtCore.QSize(250, 30))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.city.setFont(font)
        self.city.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.city.setObjectName("city")
        self.email = QtWidgets.QLineEdit(Form)
        self.email.setGeometry(QtCore.QRect(100, 280, 300, 30))
        self.email.setMinimumSize(QtCore.QSize(300, 30))
        self.email.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.email.setFont(font)
        self.email.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.email.setObjectName("email")
        self.password = QtWidgets.QLineEdit(Form)
        self.password.setGeometry(QtCore.QRect(100, 520, 300, 30))
        self.password.setMinimumSize(QtCore.QSize(300, 30))
        self.password.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.password.setFont(font)
        self.password.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.password.setMaxLength(8)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.repassword = QtWidgets.QLineEdit(Form)
        self.repassword.setGeometry(QtCore.QRect(100, 590, 300, 30))
        self.repassword.setMinimumSize(QtCore.QSize(300, 30))
        self.repassword.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.repassword.setFont(font)
        self.repassword.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.repassword.setMaxLength(8)
        self.repassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.repassword.setObjectName("repassword")
        self.sign_Button = QtWidgets.QPushButton(Form)
        self.sign_Button.setGeometry(QtCore.QRect(300, 700, 100, 50))
        self.sign_Button.setMinimumSize(QtCore.QSize(100, 50))
        self.sign_Button.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.sign_Button.setFont(font)
        self.sign_Button.setStyleSheet("sign_Button{\n"
"background-color: rgb(118, 181, 203);\n"
"}\n"
"")
        self.sign_Button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./sign/assets/signup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sign_Button.setIcon(icon)
        self.sign_Button.setIconSize(QtCore.QSize(100, 100))
        self.sign_Button.setObjectName("sign_Button")
        self.phone_number = QtWidgets.QLineEdit(Form)
        self.phone_number.setGeometry(QtCore.QRect(100, 460, 300, 30))
        self.phone_number.setMinimumSize(QtCore.QSize(300, 30))
        self.phone_number.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.phone_number.setFont(font)
        self.phone_number.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.phone_number.setPlaceholderText("")
        self.phone_number.setObjectName("phone_number")
        self.birthday = QtWidgets.QDateEdit(Form)
        self.birthday.setGeometry(QtCore.QRect(100, 340, 300, 30))
        self.birthday.setMinimumSize(QtCore.QSize(300, 30))
        self.birthday.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.birthday.setFont(font)
        self.birthday.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.birthday.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.birthday.setCalendarPopup(True)
        self.birthday.setDate(QtCore.QDate(2024, 1, 1))
        self.birthday.setObjectName("birthday")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(410, 160, 20, 20))
        self.label_2.setMinimumSize(QtCore.QSize(20, 20))
        self.label_2.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(410, 220, 20, 20))
        self.label_3.setMinimumSize(QtCore.QSize(20, 20))
        self.label_3.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(410, 280, 20, 20))
        self.label_4.setMinimumSize(QtCore.QSize(20, 20))
        self.label_4.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(410, 400, 20, 20))
        self.label_5.setMinimumSize(QtCore.QSize(20, 20))
        self.label_5.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(410, 450, 20, 20))
        self.label_6.setMinimumSize(QtCore.QSize(20, 20))
        self.label_6.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(410, 520, 20, 20))
        self.label_7.setMinimumSize(QtCore.QSize(20, 20))
        self.label_7.setMaximumSize(QtCore.QSize(20, 20))
        self.label_7.setSizeIncrement(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(410, 590, 20, 20))
        self.label_8.setMinimumSize(QtCore.QSize(20, 20))
        self.label_8.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_8.setObjectName("label_8")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(410, 340, 20, 20))
        self.label_11.setMinimumSize(QtCore.QSize(20, 20))
        self.label_11.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_11.setObjectName("label_11")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(220, 60, 61, 51))
        self.label.setStyleSheet("border-image: url(./sign/assets/add-friend.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.student_radioButton = QtWidgets.QRadioButton(Form)
        self.student_radioButton.setGeometry(QtCore.QRect(100, 640, 95, 20))
        self.student_radioButton.setStyleSheet("\n"
"background-color: rgb(57, 57, 57);\n"
"color: rgb(255, 255, 255);")
        self.student_radioButton.setObjectName("student_radioButton")
        self.teacher_radioButton = QtWidgets.QRadioButton(Form)
        self.teacher_radioButton.setGeometry(QtCore.QRect(100, 680, 95, 20))
        self.teacher_radioButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(57, 57, 57);")
        self.teacher_radioButton.setObjectName("teacher_radioButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.name.setPlaceholderText(_translate("Form", "Name"))
        self.surname.setPlaceholderText(_translate("Form", "Surname"))
        self.city.setPlaceholderText(_translate("Form", "City"))
        self.email.setPlaceholderText(_translate("Form", "Email"))
        self.password.setPlaceholderText(_translate("Form", "Password"))
        self.repassword.setPlaceholderText(_translate("Form", "Re-Password"))
        self.phone_number.setInputMask(_translate("Form", "(999)999 99 99"))
        self.label_2.setText(_translate("Form", "*"))
        self.label_3.setText(_translate("Form", "*"))
        self.label_4.setText(_translate("Form", "*"))
        self.label_5.setText(_translate("Form", "*"))
        self.label_6.setText(_translate("Form", "*"))
        self.label_7.setText(_translate("Form", "*"))
        self.label_8.setText(_translate("Form", "*"))
        self.label_11.setText(_translate("Form", "*"))
        self.student_radioButton.setText(_translate("Form", "Student"))
        self.teacher_radioButton.setText(_translate("Form", "Teacher"))

