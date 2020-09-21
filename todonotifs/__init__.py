import sqlite3
from sqlite3 import Error
import os

def create_tables(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS subjects (name TEXT PRIMARY KEY, icon TEXT);''') # todo: add option of uploading custom icon
            c.execute('''CREATE TABLE IF NOT EXISTS todos 
                        (id INTEGER NOT NULL PRIMARY KEY, name TEXT, date INTEGER, subject TEXT DEFAULT misc,
                        FOREIGN KEY(subject) REFERENCES subjects(name)
                        ON DELETE CASCADE);''')
            c.execute('''CREATE TABLE IF NOT EXISTS notifs
                        (id TEXT NOT NULL PRIMARY KEY, todo_id INTEGER, next_run_time TEXT, job_state BLOB,
                        FOREIGN KEY(todo_id) REFERENCES todos(id))''')
            c.execute(''' INSERT OR IGNORE INTO subjects(name, icon) VALUES("misc", "default_notification.ico");''')
            c.execute(''' INSERT INTO todos(name, date) VALUES(NULL, NULL);''')
            conn.commit()
            conn.close()

if __name__ == '__main__':
    create_tables(r"resources\sqlite\todos.db")