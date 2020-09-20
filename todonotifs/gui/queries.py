import sqlite3
from sqlite3 import Error

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
            data = c.fetchall()
            if len(data) == 0:
                data = c.lastrowid
            conn.commit()
            conn.close()
            print("data: ", data)
            return data

# Todos

remove_todo = '''DELETE FROM todos WHERE id=?;'''

add_todo = '''INSERT INTO todos (name, date, subject)
                VALUES (?, ?, ?);'''

edit_todo = '''UPDATE todos SET name = ?, date = ?, subject = ? WHERE id=?'''

get_all_todos = '''SELECT * FROM todos ORDER BY date;'''

# Notifications

get_all_notifs = '''SELECT * FROM notifications ORDER BY datetime;'''

add_notif = '''INSERT INTO notifications (name, date, subject, priority) 
                VALUES (?, ?, ?, ?);'''


# Subjects

change_icon = ''''''

add_subject = ''''''

remove_subject = ''''''
