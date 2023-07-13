from PyQt6.QtWidgets import QMainWindow, QStatusBar, QApplication, QLineEdit, QVBoxLayout, QLabel, QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
import sqlite3

class UpdateAdapter(QDialog):
    
    __doUpdate = None
    
    
    
    def __init__(self, window, identification, dfname, dlname, demail, dgender):
        super().__init__()
        
        self.dfname = dfname
        self.dlname = dlname
        self.demail = demail
        self.dgender = dgender
        
        self.__doUpdate = EditDialog(identification, dfname, dlname, demail, dgender)
        self.__doUpdate.set_main_window(window)
        self.__doUpdate.update_window()
    
    def execute(self):
        self.__doUpdate.exec()
        
class EditDialog(QDialog):
    __id = None
        
    def __init__(self, id, dfname, dlname, demail, dgender):
        super().__init__()
        
        self.__id = id
        
        self.dfname = dfname
        self.dlname = dlname
        self.demail = demail
        self.dgender = dgender
    
    def edit_student(self):
        name = self.student_name.text()
        lname = self.student_Lastname.text()
        gender = self.gender.itemText(self.gender.currentIndex())
        macID = self.macID.text()
        connection = sqlite3.connect("database/projectDatabase.db")
        
        cursor = connection.cursor()
        cursor.execute(''' UPDATE students
              SET first_name = ? ,
                  last_name = ? ,
                  macid = ?,
                  gender = ?
              WHERE macid = ?''', (name, lname, macID, gender, self.__id))
        
        email = self.email.text()
        cursor.execute(''' UPDATE contacts
              SET macid = ? ,
                  email = ?
              WHERE macid = ?''', (macID, email, self.__id))        
        
        connection.commit()
        cursor.close()
        connection.close()
        
        self.__mainWindow.load_data()
   
    def set_main_window(self, mainWindow):
        self.__mainWindow = mainWindow
    
    def update_window(self):
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText(self.dfname)
        layout.addWidget(self.student_name)
        
        self.student_Lastname = QLineEdit()
        self.student_Lastname.setPlaceholderText(self.dlname)
        layout.addWidget(self.student_Lastname)
        
        self.gender = QComboBox()
        
        oldList = ["Boy", "Girl"]
        
        newItems = [self.dgender]
        
        for item in oldList:
            if item != self.dgender:
                newItems.append(item)
                
        self.gender.addItems(newItems)
        layout.addWidget(self.gender)
        
        self.macID = QLineEdit()
        self.macID.setPlaceholderText(self.__id)
        layout.addWidget(self.macID)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText(self.demail)
        layout.addWidget(self.email)
        
        button = QPushButton("Update")
        button.clicked.connect(self.edit_student)
        layout.addWidget(button)
        
        self.setLayout(layout)