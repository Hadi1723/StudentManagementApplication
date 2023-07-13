import sys
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QApplication, QLineEdit, QVBoxLayout, QLabel, QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
import sqlite3

class DeleteAdapter(QDialog):
    
    __doDelete  = None
    
    def __init__(self, window, idd):
        super().__init__()
        
        self.__doDelete = DeleteDialog(idd)
        self.__doDelete.set_main_window(window)
        self.__doDelete.deleteWindow()
    
    def execute(self):
        self.__doDelete.exec()
        
class DeleteDialog(QDialog):
    
    __id = None
    __mainWindow = None
    
    def __init__(self, id):
        super().__init__()
        
        self.__id = id
    
    def delete(self):

        connection = sqlite3.connect("database/projectDatabase.db")
        
        cursor = connection.cursor()
        sql = 'DELETE FROM students WHERE macid=?'
        cursor.execute(sql, (self.__id,))
        
        sql2 = 'DELETE FROM contacts WHERE macid=?'
        cursor.execute(sql2, (self.__id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        self.__mainWindow.load_data()
    
    def set_main_window(self, mainWindow):
        self.__mainWindow = mainWindow
    
    def deleteWindow(self):
        self.setWindowTitle("Delete Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        self.name_label = QLabel("Are You sure You wanna delete?") 
        layout.addWidget(self.name_label)
        
        button = QPushButton("Delete")
        button.clicked.connect(self.delete)
        layout.addWidget(button)
        
        self.setLayout(layout)