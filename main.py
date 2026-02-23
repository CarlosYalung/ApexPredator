from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # This makes the base URL (http://127.0.0.1:5000/) load your homepage
    return render_template('homepage.html')

@app.route('/homepage.html')
def home():
    return render_template('homepage.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/tickets.html')
def tickets():
    return render_template('tickets.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)