import os
import sqlite3
from flask import g

DATABASE_PATH = os.environ.get('DB_PATH')

def connect_db():
    sql = sqlite3.connect(DATABASE_PATH)
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
