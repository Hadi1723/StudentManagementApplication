from PyQt6.QtWidgets import QMainWindow, QStatusBar, QApplication, QLineEdit, QVBoxLayout, QLabel, QWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
from adapters.insertAdapter import InsertAdapter
from adapters.deleteAdapter import DeleteAdapter
from adapters.searchAdapter import SearchAdapter
from adapters.updateAdapter import UpdateAdapter
from adapters.sendAdapter import SendAdapter
import sys

import sqlite3

#QWidget is a class that makes a GUI window
# QMainWindow used for multiple windows and menu bar

def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class MainWindow(QMainWindow):
    
    def __init__(self):
        # calling parent method
        super().__init__()
        
        ''' Setting Title for widget'''
        self.setWindowTitle("Student Management System")    
        self.setMinimumSize(800, 600)


        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        restart_menu_item = self.menuBar().addMenu("&Home")
        load_menu_item = self.menuBar().addMenu("&Search")
        
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)        
        file_menu_item.addAction(add_student_action)
        
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        
        
        restart_Action = QAction("View Whole Table", self)
        restart_Action.triggered.connect(self.load_data)
        restart_menu_item.addAction(restart_Action)
        
        search_student_action = QAction(QIcon("icons/search.png"), "Search Student", self)
        search_student_action.triggered.connect(self.search_student)        
        load_menu_item.addAction(search_student_action)
        
        
        add_student_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        restart_Action.setMenuRole(QAction.MenuRole.NoRole)
        search_student_action.setMenuRole(QAction.MenuRole.NoRole)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("First Name", "Last Name", "MACID", "Email", "Gender"))
        self.setCentralWidget(self.table)
        
        # creating toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)
        
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.table.cellClicked.connect(self.clicked_cell)
        
    
    def load_data(self):
        connection = sqlite3.connect("database/projectDatabase.db")
        
        result = connection.execute("SELECT S.first_name, S.last_name, C.macid, C.email, S.gender FROM students S Left JOIN contacts C ON S.macid = C.macid")
        
        # refreshes data
        self.table.setRowCount(0)
        
        for row, rdata in enumerate(result):
            self.table.insertRow(row)
            for column, cdata in enumerate(rdata):
                self.table.setItem(row, column, QTableWidgetItem(str(cdata)))
        
        connection.close()
    
    def clicked_cell(self):
        
        #editButton = QPushButton("Edit Record")
        #editButton.clicked.connect(self.edit)
        
        emailButton = QPushButton("Send Email")
        emailButton.clicked.connect(self.send)
        
        deleteButton = QPushButton("Delete Record")
        deleteButton.clicked.connect(self.delete)
        
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        
        #self.statusbar.addWidget(editButton)
        self.statusbar.addWidget(deleteButton)
        self.statusbar.addWidget(emailButton)
    
    def insert(self):
        dialog = InsertAdapter(app_calc)   
        dialog.execute()   
        #dialog.exec()
        
    def search_student(self):
        dialog = SearchAdapter(app_calc, self.table) 
        dialog.execute()   
        #dialog.exec()
    
    def edit(self):
        
        rowNum = self.table.currentRow()
        idd = (self.table.item(rowNum, 2).text())
        
        dialog = UpdateAdapter(app_calc,  self.table.item(rowNum, 0).text(), self.table.item(rowNum, 1).text(), idd, self.table.item(rowNum, 3).text(), self.table.item(rowNum, 4).text())
        dialog.execute()  
        #dialog.exec()
    
    def delete(self):
        rowNum = self.table.currentRow()
        idd = (self.table.item(rowNum, 2).text())
        
        dialog = DeleteAdapter(app_calc, idd)
        dialog.execute()  
        #dialog.exec()
    
    def send(self):
        rowNum = self.table.currentRow()
        choosenEmail = (self.table.item(rowNum, 3).text())
        
        dialog = SendAdapter(app_calc, choosenEmail)
        dialog.execute()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_calc = MainWindow()
    app_calc.show()
    
    app_calc.load_data()
    
    sys.exit(app.exec())