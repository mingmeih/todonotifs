import sqlite3
from sqlite3 import Error
import dateutil.parser as parser

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

def run_query(query, params):
    try:
        conn = sqlite3.connect(r"resources\sqlite\notifs.db")
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            c = conn.cursor()
            print(params)
            c.execute(query, params)
            if query.startswith('SELECT'):
                data = c.fetchall()
            else:
                data = c.lastrowid
            conn.commit()
            conn.close()
            return data

# Todos

remove_todo = '''DELETE FROM todos WHERE id=?;'''

add_todo = '''INSERT INTO todos (name, date, subject)
                VALUES (?, ?, ?);'''

edit_todo = '''UPDATE todos SET name = ?, date = ?, subject = ? WHERE id=?'''

get_all_todos = '''SELECT * FROM todos ORDER BY date;'''

# Notifications

get_all_notifs = '''SELECT * FROM notifications ORDER BY datetime;'''

get_notif_by_todo = '''SELECT * FROM notifications WHERE "todo-id" = ?;'''

add_notif = '''INSERT INTO notifications ("todo-id", datetime) 
                VALUES (?, ?);'''


# Subjects

change_icon = ''''''

add_subject = ''''''

remove_subject = ''''''
