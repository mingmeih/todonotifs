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
            c.execute('''CREATE TABLE IF NOT EXISTS subjects (name TEXT PRIMARY KEY, icon TEXT);''')
            c.execute('''CREATE TABLE IF NOT EXISTS todos 
                        (id INTEGER NOT NULL PRIMARY KEY, name TEXT, date INTEGER, subject TEXT DEFAULT misc,
                        FOREIGN KEY(subject) REFERENCES subjects(name)
                        ON DELETE CASCADE);''')
            c.execute('''CREATE TABLE IF NOT EXISTS notifications 
                        ("todo-id" INTEGER NOT NULL PRIMARY KEY, datetime INTEGER, message TEXT DEFAULT "Upcoming task!", repeat INTEGER DEFAULT 0,
                        FOREIGN KEY("todo-id") REFERENCES todos(id))''')
            c.execute(''' INSERT OR IGNORE INTO subjects(name, icon) VALUES("misc", "default_notification.ico");''')
            conn.commit()
            conn.close()

if __name__ == '__main__':
    create_tables(r"resources\sqlite\notifs.db")