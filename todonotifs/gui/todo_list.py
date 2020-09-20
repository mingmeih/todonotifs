import sqlite3 as lite
import dateutil.parser as parser
import datetime

import todonotifs.gui.queries as queries
import todonotifs.notif as notif

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit, QStyle, QVBoxLayout
from collections import OrderedDict

def to_iso(datestr):
    if datestr:
        date = parser.parse(datestr)
        return date.isoformat()
    else:
        return None

def is_valid_date(datestr):
    try:
        return to_iso(datestr)
    except:
        return False

def valid_todo(todo_str):
    params = OrderedDict.fromkeys(['name', 'date', 'subject'])
    items = todo_str.split(' - ')
    length = len(items)
    if length == 1:
        if items[0] == "":
            return False
        params['name'] = items[0]
    elif length == 2:
        if is_valid_date(items[0]):
            params['date'] = to_iso(items[0])
            params['name'] = items[1]
        else:
            params['subject'] = items[0]
            params['name'] = items[1]
    elif length == 3:
        params['date'] = to_iso(items[0])
        params['subject'] = items[1]
        params['name'] = items[2]
    else:
        return False
    return params


def add_todo(todo_str):
    params = valid_todo(todo_str)
    if params:
        queries.run_query(queries.add_todo, list(params.values()))
        print(params)
        notif.sched.add_job()



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
            datetime = parser.parse(self.date)
            date_string = datetime.strftime("%a %b %d %I:%M %p")
        todo_attrs = [date_string, self.subject, self.name]
        self.setText(" - ".join(filter(bool, todo_attrs)))

    def focusOutEvent(self, event):
        print(self.date)
        print(self.text())
        print(valid_todo(self.text()))
        params = valid_todo(self.text())
        if params:
            queries.run_query(queries.edit_todo, list(params.values()) + [self.id])
            if params['date'] != self.date:
                notif.add_notification(params)


        elif self.text().strip() == "":
                queries.run_query(queries.remove_todo, [self.id])
                self.parent_list.todo_items = [item for item in self.parent_list.todo_items if item[0] != self.id]
                self.hide()

        super().focusOutEvent(event)
        # if subject not in list of subjects, add it
        # add notifications:
        # if there is no date, set notifications to repeat daily(?) at 6 pm
        # by default: one week in advance, 3 days in advance, one day in advance, 6 hours in advance
        # save todo

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Down:

            if self.id == self.parent_list.todo_items[-1][0]:
                new_id = queries.run_query(queries.add_todo, [None, None, None])
                print("new_id:", new_id)
                params = (new_id, None, None, None)
                self.parent_list.todo_items.append(params)
                new = Todo_item(*params, self.parent_list)
                self.parent_list.addWidget(new)
                new.show()
                
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