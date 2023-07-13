import sys
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QApplication, QLineEdit, QVBoxLayout, QLabel, QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
import sqlite3

class InsertAdapter(QDialog):
    
    __doInsert = None
    
    def __init__(self, window):
        super().__init__()
        
        self.__doInsert = InsertDialog()
        self.__doInsert.set_main_window(window)
        self.__doInsert.add_window()
    
    def execute(self):
        self.__doInsert.exec()
    
class InsertDialog(QDialog):
    
    __mainWindow = None
    
    def __init__(self):
        super().__init__()
    
    def add_student(self):
        name = self.student_name.text()
        lname = self.student_Lastname.text()
        gender = self.gender.itemText(self.gender.currentIndex())
        macID = self.macID.text()
        
        email = self.email.text()
        
        connection = sqlite3.connect("database/projectDatabase.db")
        
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (FIRST_NAME, LAST_NAME, MACID, GENDER) VALUES (?,?,?, ?)", (name, lname, macID, gender))
        cursor.execute("INSERT INTO contacts (MACID, EMAIL) VALUES (?,?)", (macID, email))
        connection.commit()
        cursor.close()
        connection.close()
        
        self.__mainWindow.load_data()
    
    def set_main_window(self, mainWindow):
        self.__mainWindow = mainWindow
    
    def add_window(self):
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("First Name")
        layout.addWidget(self.student_name)
        
        self.student_Lastname = QLineEdit()
        self.student_Lastname.setPlaceholderText("Last Name")
        layout.addWidget(self.student_Lastname)
        
        self.gender = QComboBox()
        self.gender.addItems(["Boy", "Girl"])
        layout.addWidget(self.gender)
        
        self.macID = QLineEdit()
        self.macID.setPlaceholderText("MacID")
        layout.addWidget(self.macID)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("email@gmail.com")
        layout.addWidget(self.email)
        
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        
        self.setLayout(layout)