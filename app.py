from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            query TEXT,
            followup_date TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM clients")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    query = request.form['query']
    followup = request.form['followup']
    status = "Pending"

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO clients (name, query, followup_date, status) VALUES (?, ?, ?, ?)",
              (name, query, followup, status))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
