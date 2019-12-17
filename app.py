import os
from flask import Flask, render_template, g
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.environ('DB_PATH')

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect(DATABASE_PATH)
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/day')
def day():
    return render_template('day.html')

@app.route('/add_food')
def food():
    return render_template('food.html')

if __name__ == '__main__':
    app.run(debug=True)

