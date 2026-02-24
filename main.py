from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'apex_predator_secret'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    user = None
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
    return render_template('homepage.html', user=user)

@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
                     (first_name, last_name, email, password))
        conn.commit()
        # Auto-login after signup
        user = conn.execute('SELECT last_insert_rowid() as id').fetchone()
        session['user_id'] = user['id']
        return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        return "Error: This email is already registered."
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                        (email, password)).fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        return redirect(url_for('index'))
    else:
        return "Invalid email or password."

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Helper routes for your other pages
# --- FIX STARTS HERE ---

@app.route('/fighters.html')
def fighters():
    return render_template('fighters.html')

@app.route('/tickets.html')
def tickets():
    return render_template('tickets.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# DELETE the old @app.route('/homepage.html') block entirely.
# Instead, add this REDIRECT so if someone types /homepage.html,
# it sends them to the correct '/' route.
@app.route('/homepage.html')
def go_home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

