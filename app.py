import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Function to initialize the database and create tables
def init_db():
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    # Create the flights table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS flights (
                        id INTEGER PRIMARY KEY,
                        origin TEXT,
                        destination TEXT,
                        price REAL)''')
    
    # Create the bookings table
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        departure TEXT,
                        arrival TEXT,
                        flight_time TEXT)''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call init_db to make sure the tables are created when the app starts
init_db()

# This function creates a connection to the database for further use
def get_db_connection():
    conn = sqlite3.connect('booking.db')
    conn.row_factory = sqlite3.Row  # This makes it easier to work with rows as dictionaries
    return conn

@app.route('/')
def index():
    # Get flight options from the database to show on the homepage
    conn = get_db_connection()
    flights = conn.execute('SELECT * FROM flights').fetchall()
    conn.close()
    return render_template('index.html', flights=flights)

@app.route('/book', methods=['POST'])
def book():
    # Get the user’s input from the booking form
    name = request.form['name']
    email = request.form['email']
    departure = request.form['departure']
    arrival = request.form['arrival']
    flight_time = request.form['flight_time']
    
    # Add the booking to the database
    conn = get_db_connection()
    conn.execute('INSERT INTO bookings (name, email, departure, arrival, flight_time) VALUES (?, ?, ?, ?, ?)',
                 (name, email, departure, arrival, flight_time))
    conn.commit()
    conn.close()
    
    # Show the success page with the user's name
    return render_template('success.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
