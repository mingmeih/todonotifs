from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QLabel, QVBoxLayout, QPushButton, QLineEdit, QGroupBox
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
from todonotifs.gui.todo_list import Todo_item_list, to_iso

import todonotifs.gui.queries as queries
import sys 
import dateutil.parser
import random

class Todo_buttons:
    def __init__(self, todo_id):
        super().__init__()

class Window(QWidget):
    def __init__(self): 
        super().__init__() 
        vbox = Todo_item_list()
        my_groupbox = QGroupBox()
        my_groupbox.setStyleSheet("border: none;")


        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        button.clicked.connect(self.on_click)
        
        self.setWindowIcon(QtGui.QIcon(r"resources\icons\default_notification.ico"))
        self.setWindowTitle("Todo List") 
        
        scroll = QScrollArea()
        scroll.setWidget(my_groupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)

        my_groupbox.setLayout(vbox)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        layout.addWidget(button)


        self.setGeometry(0, 0, 400, 600) 
  
        self.show()

    @pyqtSlot()
    def on_click(self):
        queries.run_query(queries.add_todo, ("GET REKD", to_iso(random.choice([None, "Sept 30", "Friday", "Oct 31"])), "pasta"))
        
    


def main():

    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    window = Window()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()