from PyQt6.QtWidgets import QMainWindow, QStatusBar, QApplication, QLineEdit, QVBoxLayout, QLabel, QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
import sqlite3
import smtplib, ssl

class SendAdapter(QDialog):
    
    __mail = None
    
    def __init__(self, window, email):
        super().__init__()
        
        self.__mail = SendDialog(email)
        self.__mail.set_main_window(window)
        self.__mail.writeMail()
    
    def execute(self):
        self.__mail.exec()

class SendDialog(QDialog):
    
    __email = None
    __mainWindow = None
        
    def __init__(self, email):
        super().__init__()
        
        self.__email = email
    
    def send_email(self):
        
        body = "Subject: " + self.subject.text() + "\n" + self.textbox.text()

        body = body.encode("utf-8")
        
        host = "smtp.gmail.com"
        port = 465

        username = "hadiisb6i@gmail.com"
        password = "gqtkpvyultpdyltd"

        receiver = self.__email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, body)
    
    def set_main_window(self, mainWindow):
        self.__mainWindow = mainWindow
    
    def writeMail(self):
        self.setWindowTitle("Writing email to student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        # Create textbox
        title = QLabel("Subject: ")
        self.subject = QLineEdit(self)
        self.subject.move(20, 20)
        self.subject.resize(280,100)
        layout.addWidget(title)
        layout.addWidget(self.subject)
        
        # Create textbox
        date_label = QLabel("Message: ")
        self.textbox = QLineEdit(self)
        self.textbox.move(40, 20)
        self.textbox.resize(280,100)
        layout.addWidget(date_label)
        layout.addWidget(self.textbox)
        
        button = QPushButton("Send")
        button.clicked.connect(self.send_email)
        layout.addWidget(button)
        
        self.setLayout(layout)