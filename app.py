#!/usr/bin/env python3

from authentication.auth_tools import login_pipeline, update_passwords, hash_password
from database.db import Database
from flask import Flask, render_template, request
from core.session import Sessions

app = Flask(__name__)
HOST, PORT = 'localhost', 8080
global username, products, db, sessions
username = 'default'
db = Database('database/store_records.db')
products = db.get_full_inventory()
sessions = Sessions()
sessions.add_new_session(username, db)


@app.route('/')
def index_page():
    """
    Renders the index page when the user is at the `/` endpoint, passing along default flask variables.

    args:
        - None

    returns:
        - None
    """
    return render_template('index.html', username=username, products=products, sessions=sessions)

@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Renders the home page when the user is at the `/home` endpoint.

    args:
        - None

    returns:
        - None

    modifies:
        - sessions: adds a new session to the sessions object
    """
    global username
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_pipeline(username, password):
            sessions.add_new_session(username, db)
            return render_template('home.html', username=username, products=products, sessions=sessions)
        else:
            print(f"Incorrect username ({username}) or password ({password}).")
            return render_template('index.html')
    else:
        # This is a GET request, so render the login page
        return render_template('login.html')


@app.route('/cart')
def view_cart():
    """
    Renders the cart page when the user is at the `/cart` endpoint.

    args:
        - None

    returns:
        - None
    """
    global username  # Add this line to indicate that 'username' is a global variable
    user_session = sessions.get_session(username)
    return render_template('cart.html', username=username, sessions=sessions)


@app.route('/home', methods=['POST'])
def login():
    """
    Renders the home page when the user is at the `/home` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - sessions: adds a new session to the sessions object
    """
    global username  # Add this line to indicate that 'username' is a global variable
    username = request.form['username']
    password = request.form['password']
    if login_pipeline(username, password):
        sessions.add_new_session(username, db)
        return render_template('home.html', username=username, products=products, sessions=sessions)
    else:
        print(f"Incorrect username ({username}) or password ({password}).")
        return render_template('index.html')




@app.route('/register')
def register_page():
    """
    Renders the register page when the user is at the `/register` endpoint.

    args:
        - None

    returns:
        - None
    """
    return render_template('register.html')


@app.route('/home', methods=['POST'])
def process_login():
    """
    Renders the home page when the user is at the `/home` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - sessions: adds a new session to the sessions object
    """
    global username  # Add this line to indicate that 'username' is a global variable
    username = request.form['username']
    password = request.form['password']
    if login_pipeline(username, password):
        sessions.add_new_session(username, db)
        return render_template('home.html', username=username, products=products, sessions=sessions)
    else:
        print(f"Incorrect username ({username}) or password ({password}).")
        return render_template('index.html')




# ... (previous code)

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Renders the checkout page when the user is at the `/checkout` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - sessions: adds items to the user's cart
    """
    order = {}
    user_session = sessions.get_session(username)
    for item in products:
        print(f"item ID: {item['id']}")
        if request.form[str(item['id'])] > '0':
            count = int(request.form[str(item['id'])])  # Convert to int
            order[item['item_name']] = count
            user_session.add_new_item(
                item['id'], item['item_name'], item['price'], count)

    user_session.submit_cart()

    return render_template('checkout.html', order=order, sessions=sessions, total_cost=user_session.total_cost)

@app.route('/logout', methods=['POST'])
def logout():
    """
    Logs out the user and redirects to the login page.

    args:
        - None

    returns:
        - Redirect to the login page.
    """
    sessions.remove_session(username)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
