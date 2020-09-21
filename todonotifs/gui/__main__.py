from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QLabel, QVBoxLayout, QLineEdit, QGroupBox
from PyQt5.QtSql import QSqlDatabase
from PyQt5 import QtGui
from todonotifs.gui.todo_list import Todo_item_list

import todonotifs.queries as queries
import todonotifs.notif as notif
import sys 
import dateutil.parser

class Window(QWidget):
    def __init__(self): 
        super().__init__() 
        vbox = Todo_item_list()
        my_groupbox = QGroupBox()
        my_groupbox.setStyleSheet("border: none;")
        
        self.setWindowIcon(QtGui.QIcon(r"resources\icons\default_notification.ico"))
        self.setWindowTitle("Todo List") 
        
        scroll = QScrollArea()
        scroll.setWidget(my_groupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)

        my_groupbox.setLayout(vbox)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

        self.setGeometry(0, 0, 400, 600) 
        self.show()
        

def main():
    notif.start()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()