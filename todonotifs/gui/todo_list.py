import sqlite3 as lite
import dateutil.parser as parser
from datetime import datetime, timedelta

import todonotifs.queries as queries
import todonotifs.notif as notif

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit, QStyle, QVBoxLayout
from collections import OrderedDict

DEFAULT_NOTIF_TIMES = (timedelta(weeks = 1), timedelta(days = 3), timedelta(days = 1), timedelta(hours = 6), timedelta(hours = 1))
EMPTY_PARAMS = OrderedDict.fromkeys(['name', 'date', 'subject'])

# todo: add more error handling 
def valid_todo(todo_str):
    params = EMPTY_PARAMS
    items = todo_str.split(' - ')
    length = len(items)
    if length == 1:
        if items[0] == "":
            return False
        params['name'] = items[0]
    elif length == 2:
        if queries.is_valid_date(items[0]):
            params['date'] = queries.to_iso(items[0])
            params['name'] = items[1]
        else:
            params['subject'] = items[0]
            params['name'] = items[1]
    elif length == 3:
        params['date'] = queries.to_iso(items[0])
        params['subject'] = items[1]
        params['name'] = items[2]
    else:
        return False
    return params


class Todo_item(QLineEdit):
    def __init__(self, id: int, name: str, date: str, subject: str, parent_list):
        super().__init__()
        self.parent_list = parent_list
        self.id = id
        self.name = name
        self.subject = subject
        self.date = date
        self.setStyleSheet("""border: none; background: transparent;""")
        self.setFont(QtGui.QFont('Arial', 12))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        date_string = None
        if self.date:
            date_time = parser.parse(self.date)
            date_string = date_time.strftime("%a %b %d %I:%M %p")
        todo_attrs = [date_string, self.subject, self.name]
        self.setText(" - ".join(filter(bool, todo_attrs)))

    def create_empty_todo(self):
        new_id = queries.run_query(queries.add_todo, (None, None, None))
        new_todo = (new_id, None, None, None)
        self.parent_list.todo_items.append(new_todo)
        new = Todo_item(*new_todo, self.parent_list)
        self.parent_list.addWidget(new)
        new.show()
        
    
    def delete_todo(self):
        queries.run_query(queries.remove_todo, [self.id])
        self.parent_list.todo_items = [item for item in self.parent_list.todo_items if item[0] != self.id]
        self.hide()

    def focusOutEvent(self, event):

        super().focusOutEvent(event)
        
        params = valid_todo(self.text())
        if params:
            queries.run_query(queries.edit_todo, list(params.values()) + [self.id])
            if params['date'] != self.date:
                notif.delete_notifications(self.id)
                for time in DEFAULT_NOTIF_TIMES:
                    notif_time = parser.parse(params['date']) - time
                    if notif_time > datetime.now():
                        notif.add_notification(params, self.id, notif_time)

        elif self.text().strip() == "":
                self.delete_todo()


    def keyPressEvent(self, event):
        
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Down:
            
            if self.id == self.parent_list.todo_items[-1][0]:
                self.create_empty_todo()
            self.parent().focusNextChild()

        elif event.key() == QtCore.Qt.Key_Up:
            self.parent().focusPreviousChild()
        else:
            QLineEdit.keyPressEvent(self, event)


class Todo_item_list(QVBoxLayout):
    def __init__(self): 
        super().__init__()
        self.todo_items = queries.run_query(queries.get_all_todos, ())
        for i in self.todo_items:
            self.addWidget(Todo_item(*i, self))
        if len(self.todo_items) == 0:
            self.addWidget