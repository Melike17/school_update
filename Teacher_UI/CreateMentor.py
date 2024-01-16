import sys, os
sys.path.append(os.getcwd())

from Classes.user import User
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class CreateMentor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Mentoring")
        self.setGeometry(100, 100, 400, 300)

        self.init_ui()

    def init_ui(self):
     
        self.label_gun = QLabel("Mentoring Date:")
        self.textbox_gun = QLineEdit()

        self.label_ders = QLabel("Mentoring Subject:")
        self.textbox_ders = QLineEdit()

        self.label_baslama = QLabel("Mentoring Start Time:")
        self.textbox_baslama = QLineEdit()

        self.label_bitis = QLabel("Mentoring Finish Time:")
        self.textbox_bitis = QLineEdit()

        self.button_kaydet = QPushButton("Save")
        self.button_kaydet.clicked.connect(self.kaydet)

        # Layout oluştur
        layout = QVBoxLayout()
        layout.addWidget(self.label_gun)
        layout.addWidget(self.textbox_gun)
        layout.addWidget(self.label_ders)
        layout.addWidget(self.textbox_ders)
        layout.addWidget(self.label_baslama)
        layout.addWidget(self.textbox_baslama)
        layout.addWidget(self.label_bitis)
        layout.addWidget(self.textbox_bitis)
        layout.addWidget(self.button_kaydet)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def kaydet(self):
        date = self.textbox_gun.text()
        mentor = self.textbox_ders.text()
        start = self.textbox_baslama.text()
        finish = self.textbox_bitis.text()

        User.create_mentor([date, mentor, start, finish])
        self.close()

def ders_planini_al():
    app = QApplication(sys.argv)
    pencere = CreateMentor()
    pencere.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    ders_planini_al()