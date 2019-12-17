import os
import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.environ.get('DB_PATH')

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
        
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/day')
def day():
    return render_template('day.html')

@app.route('/food', methods=['GET', 'POST'])
def food():
    db = get_db()
    
    if request.method == 'POST':
        name = request.form['name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])
        calories = protein * 4 + carbohydrates * 4 + fat * 9
        
        db.execute('insert into food (name, protein, carbohydrates, fat, calories) values (?, ?, ?, ?, ?)', [name, protein, carbohydrates, fat, calories])
        db.commit()

        return redirect(url_for('food'))

    cur = db.execute('select name, protein, carbohydrates, fat, calories from food')
    results = cur.fetchall()
    
    return render_template('food.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

