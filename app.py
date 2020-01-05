import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, g, request, redirect, url_for
from dotenv import load_dotenv

from db import get_db, connect_db

load_dotenv()

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    
    if request.method == 'POST':
        date = request.form['date']
        dtime = datetime.strptime(date, '%Y-%m-%d')
        insert_date = datetime.strftime(dtime, '%Y%m%d')

        db.execute('insert into log_date (entry_date) values (?)', [insert_date])
        db.commit()

    query = db.execute('select log_date.entry_date, sum(food.fat) as fat, sum(food.protein) as protein, sum(food.carbohydrates) as carbohydrates, sum(food.calories) as calories from log_date join food_date on food_date.log_date_id = log_date.id join food on food.id = food_date.food_id group by log_date.id order by log_date.entry_date desc')
    results = query.fetchall()

    date_list = []
    for i in results:
        date = {}
        dtime = datetime.strptime(str(i['entry_date']), '%Y%m%d')
        date['entry_date'] = datetime.strftime(dtime, '%B %d, %Y')
        date['protein'] = i['protein']
        date['fat'] = i['fat']
        date['carbohydrates'] = i['carbohydrates']
        date['calories'] = i['calories']
        date_list.append(date)
        
    return render_template('home.html', dates=date_list)

@app.route('/day/<date>', methods=['GET', 'POST'])
def day(date):
    db = get_db()

    try:
        date_input = int(date)
    except ValueError:
        date_parsed_from_url = datetime.strptime(date, '%B %d, %Y')
        date_input = int(datetime.strftime(date_parsed_from_url, '%Y%m%d'))
        
    date_query = db.execute('select id, entry_date from log_date where entry_date = (?)', [date_input])
    date_entry = date_query.fetchone()
    
    if request.method == 'POST':
        db.execute('insert into food_date (food_id, log_date_id) values (?, ?)', [request.form['food'], date_entry['id']])
        db.commit()
    
    dtime = datetime.strptime(str(date_entry['entry_date']), '%Y%m%d')
    pretty_date = datetime.strftime(dtime, '%B %d, %Y')

    food_query = db.execute('select id, name from food')
    food = food_query.fetchall()

    food_results = []
    for f in food:
        food_results.append({'id': f['id'], 'name': f['name']})

    log_query = db.execute('select food.name, food.fat, food.protein, food.carbohydrates, food.calories from log_date join food_date on food_date.log_date_id = log_date.id join food on food.id = food_date.food_id where log_date.entry_date = ?', [date_input])
    log_results = log_query.fetchall()

    totals = {
        'protein': 0,
        'carbohydrates': 0,
        'fat': 0,
        'calories': 0
    }
    
    for food in log_results:
        totals['protein'] += food['protein']
        totals['carbohydrates'] += food['carbohydrates']
        totals['fat'] += food['fat']
        totals['calories'] += food['calories']
    
    return render_template('day.html', date=pretty_date, food=food_results, food_log=log_results, totals=totals)

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

