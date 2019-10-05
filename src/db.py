import logging
import os
import sqlite3

db_file_path = ''


def set_db(path=None):
    global db_file_path
    if path:
        db_file_path = path
        logging.info(f'DB module initialization. dbFile path is: {db_file_path}')
    else:
        db_file_path = os.getcwd() + '\\db\\user-database.db'
        logging.info(f'DB module initialization with default dbFile path: {db_file_path}')


def create_connection():
    if not os.path.exists(db_file_path):
        logging.warning('DB file is not found. New DB Will be created')
    conn = sqlite3.connect(db_file_path)
    conn.row_factory = sqlite3.Row
    return conn


def transaction(input_func):
    def decorator(conn=None, **kwargs):
        if not conn:
            conn = create_connection()
        c = conn.cursor()

        output = input_func(c, **kwargs)

        conn.commit()
        conn.close()
        return output
    return decorator


@transaction
def create_user_tables(c=None):
    c.execute('''CREATE TABLE IF NOT EXISTS user
                 (name text PRIMARY KEY, password text NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat
                 (id INTEGER PRIMARY KEY, user text NOT NULL)''')


@transaction
def add_user(c=None,  **kwargs):
    c.execute('''INSERT OR IGNORE INTO user 
                     VALUES (:user, :password)''', kwargs)


@transaction
def is_authenticated(c=None,  **kwargs):
    c.execute('select * from chat WHERE id=:chat_id', kwargs)
    row = c.fetchone()
    if row:
        logging.info(f'chat:{kwargs["chat_id"]} is registered')
        return row['user']
    else:
        logging.info(f'chat:{kwargs["chat_id"]} is not found')
        return False


@transaction
def bind_chat_to_user(c=None,  **kwargs):
    c.execute('''INSERT OR IGNORE INTO chat 
                VALUES (:chat_id, :user)''', kwargs)


@transaction
def is_user_exists(c=None,  **kwargs):
    c.execute('select * from user WHERE name=:user_name and password = :user_pass', kwargs)
    row = c.fetchone()
    if row:
        return True
    else:
        return False
