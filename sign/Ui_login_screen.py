
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\MainUser\Documents\GitHub\school-management-system\sign\login_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 400)
        Form.setMinimumSize(QtCore.QSize(300, 400))
        Form.setMaximumSize(QtCore.QSize(300, 400))
        Form.setStyleSheet("background-color: rgb(57, 57, 57);")
        self.enter_Button = QtWidgets.QPushButton(Form)
        self.enter_Button.setGeometry(QtCore.QRect(20, 180, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.enter_Button.setFont(font)
        self.enter_Button.setStyleSheet("background-color: rgb(0, 255, 127);\n"
"font: 8pt \"Comic Sans MS\";\n"
"")
        self.enter_Button.setObjectName("enter_Button")
        self.password = QtWidgets.QLineEdit(Form)
        self.password.setGeometry(QtCore.QRect(20, 120, 250, 30))
        self.password.setMinimumSize(QtCore.QSize(250, 30))
        self.password.setMaximumSize(QtCore.QSize(250, 30))
        self.password.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.password.setInputMask("")
        self.password.setText("")
        self.password.setMaxLength(8)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.email = QtWidgets.QLineEdit(Form)
        self.email.setGeometry(QtCore.QRect(20, 60, 250, 30))
        self.email.setMinimumSize(QtCore.QSize(250, 30))
        self.email.setMaximumSize(QtCore.QSize(250, 30))
        self.email.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.email.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly)
        self.email.setText("")
        self.email.setMaxLength(32764)
        self.email.setObjectName("email")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 260, 81, 61))
        self.label.setStyleSheet("border-image: url(./sign/assets/login.png);\n"
"")
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.enter_Button.setText(_translate("Form", "LOGIN"))
        self.password.setPlaceholderText(_translate("Form", "Enter a valid password"))
        self.email.setPlaceholderText(_translate("Form", "Enter a valid email"))
