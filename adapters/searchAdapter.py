from PyQt6.QtWidgets import QMainWindow, QStatusBar, QApplication, QLineEdit, QVBoxLayout, QLabel, QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
import sqlite3

class SearchAdapter(QDialog):
    
    __doSearch = None
    
    def __init__(self, window, table):
        super().__init__()
        
        self.__doSearch = SearchDialog(table)
        self.__doSearch.set_main_window(window)
        self.__doSearch.lookup()
    
    def execute(self):
        self.__doSearch.exec()

class SearchDialog(QDialog):
    
    __table = None
    __mainWindow = None
        
    def __init__(self, table):
        super().__init__()
        
        self.__table = table
    
    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database/projectDatabase.db")
        
        queryName = "%"+name+"%"
        
        result = connection.execute("SELECT S.first_name, S.last_name, C.macid, C.email, S.gender  FROM students S Left JOIN contacts C ON S.macid = C.macid WHERE S.macid like ?", (queryName,))
        
        # refreshes data
        self.__table.setRowCount(0)
        
        for row, rdata in enumerate(result):
            self.__table.insertRow(row)
            for column, cdata in enumerate(rdata):
                self.__table.setItem(row, column, QTableWidgetItem(str(cdata)))
        
        connection.close()
    
    def set_main_window(self, mainWindow):
        self.__mainWindow = mainWindow
    
    def lookup(self):
        self.setWindowTitle("Search Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("MACID")
        layout.addWidget(self.student_name)
        
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)
        
        self.setLayout(layout)