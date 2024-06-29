# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3 as sql
import traceback

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

data_base = r'bike_rental.db'

# Database setup
def init_db():
    con = sql.connect(data_base)
    with con:
        con.execute('''CREATE TABLE IF NOT EXISTS my_database
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(255),
                        email VARCHAR(255),
                        password VARCHAR(255))''')
    con.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            con = sql.connect(data_base)
            cur = con.cursor()
            cur.execute('''SELECT email FROM my_database WHERE email=?''', (email,))
            if cur.fetchone():
                flash("Email already exists. Please log in.")
                return redirect(url_for('login'))

            cur.execute('''INSERT INTO my_database (name, email, password) VALUES (?, ?, ?)''',
                        (name, email, password))
            con.commit()
            con.close()
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred during registration: {e}")
            traceback.print_exc()
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            con = sql.connect(data_base)
            cur = con.cursor()
            cur.execute('''SELECT password FROM my_database WHERE email=?''', (email,))
            result = cur.fetchone()
            con.close()

            if result and result[0] == password:
                session['email'] = email
                flash("Login successful!")
                return redirect(url_for('index'))
            else:
                flash("Invalid email or password.")
        except Exception as e:
            flash(f"Something went wrong. Please try again: {e}")
            traceback.print_exc()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))

@app.route('/bikes', methods=['GET'])
def bikes_available():
    return render_template('book_bike.html', bikes={
        'Pulsar': 20,
        'Apache': 15,
        'R15': 13
    })

@app.route('/book', methods=['POST'])
def book_bike():
    if 'email' not in session:
        flash("Please log in to book a bike.")
        return redirect(url_for('login'))

    try:
        bike_type = request.form['bike_type']
        quantity = int(request.form['quantity'])
        hours = int(request.form['hours'])
        
        if bike_type == 'Pulsar':
            amount = quantity * hours * 70
        elif bike_type == 'Apache':
            amount = quantity * hours * 60
        elif bike_type == 'R15':
            amount = quantity * hours * 90
        else:
            flash("Invalid bike type selected.")
            return redirect(url_for('bikes_available'))

        flash(f"You have booked {quantity} {bike_type}(s) for {hours} hours. Total amount: Rs.{amount}")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An error occurred during booking: {e}")
        traceback.print_exc()
        return redirect(url_for('bikes_available'))

@app.route('/query', methods=['GET', 'POST'])
def query():
    if 'email' not in session:
        flash("Please log in to submit a query.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            query_text = request.form['query']
            query_id = generate_query_id()
            # Save the query details to database or file
            flash(f"Your query has been submitted. Your query ID is {query_id}.")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"An error occurred while submitting your query: {e}")
            traceback.print_exc()
            return redirect(url_for('query'))

    return render_template('query.html')

# Function to generate query ID
def generate_query_id():
    import random
    return random.randint(1000, 10000)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
