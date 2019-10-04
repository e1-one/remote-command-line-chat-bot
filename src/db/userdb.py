import logging
import sqlite3
import os


db_file_path = os.getcwd() + '\\db\\user-database.db'

def set_db(path):
    db_file_path = path

def create_connection():
    if not os.path.exists(db_file_path):
        logging.warning('DB file is not found. New DB Will be created')
    conn = sqlite3.connect(db_file_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_user_tables():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user
                 (name text PRIMARY KEY, password text NOT NULL, role text NOT NULL, cwd text )''')
    c.execute('''INSERT OR IGNORE INTO user 
                 VALUES ('admin','qwerty','ADMIN', 'C://')''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat
                 (id INTEGER PRIMARY KEY, user text NOT NULL)''')
    conn.commit()
    conn.close()


def is_authenticated(chat_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('select * from chat WHERE id=?', (chat_id,))
    row = c.fetchone()
    conn.close()
    if row:
        logging.info(f'chat:{chat_id} is registered')
        # Chat(row['id'], row['first_name'], row['user'])
        return row['user']
    else:
        logging.info(f'chat:{chat_id} not found')
        return False


def get_working_directory(user):
    conn = create_connection()
    c = conn.cursor()
    c.execute('select * from user WHERE name=?', (user,))
    row = c.fetchone()
    conn.commit()
    conn.close()
    return row['cwd']


def update_working_directory(user, dir):
    conn = create_connection()
    c = conn.cursor()
    c.execute('UPDATE user  SET cwd=? WHERE name=?', (dir, user,))
    conn.commit()
    conn.close()


def bind_chat_to_user(chat_id, user):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO chat 
                   VALUES (?,?)''', (chat_id, user))
    conn.commit()
    conn.close()


def is_user_exists(user_name, user_pass):
    conn = create_connection()
    c = conn.cursor()
    c.execute('select * from user WHERE name=? and password = ?', (user_name, user_pass))
    row = c.fetchone()

    conn.close()
    if row:
        return True
    else:
        return False
