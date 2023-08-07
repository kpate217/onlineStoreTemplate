#!/usr/bin/env python3

from authentication.auth_tools import login_pipeline, update_passwords, hash_password
from database.db import Database
from flask import Flask, render_template, request, redirect
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


@app.route('/login')
def login_page():
    """
    Renders the login page when the user is at the `/login` endpoint.

    args:
        - None

    returns:
        - None
    """
    return render_template('login.html')


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
    username = request.form['username']
    password = request.form['password']
    if login_pipeline(username, password):
        sessions.add_new_session(username, db)
        return render_template('home.html', products=products, sessions=sessions)
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


@app.route('/register', methods=['POST'])
def register():
    """
    Renders the index page when the user is at the `/register` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - passwords.txt: adds a new username and password combination to the file
        - database/store_records.db: adds a new user to the database
    """
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    salt, key = hash_password(password)
    update_passwords(username, key, salt)
    db.insert_user(username, key, email, first_name, last_name)
    return render_template('index.html')


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
    tax_rate = 0.07  # 7% tax rate
    subtotal = 0

    for item in products:
        item_id = str(item['id'])
        quantity_str = request.form.get(item_id, '')
        try:
            quantity = int(quantity_str)
        except ValueError:
            quantity = 0

        if quantity > 0:
            price = float(item['price'])
            total_price = price * quantity
            order[item['item_name']] = {
                'quantity': quantity,
                'price': price,
                'total': total_price
            }
            subtotal += total_price

    tax = subtotal * tax_rate
    grand_total = subtotal + tax

    discount_code = request.form.get('discount_code', '')
    discount_code_applied = False
    discount_amount = 0

    if discount_code.lower() == 'tenoff':
        discount_code_applied = True
        discount_amount = subtotal * 0.10  # 10% discount

    grand_total -= discount_amount

    return render_template('checkout.html', order=order, tax=tax, grand_total=grand_total, discount_code=discount_code, discount_code_applied=discount_code_applied, discount_amount=discount_amount, subtotal=subtotal)


@app.route('/contact', methods=['GET'])
def contact_us():
    # Add any necessary logic or data processing here
    return render_template('contact_us.html')  # This renders the contact_us.html template

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # Retrieve the submitted form data
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Add any necessary logic or data processing here

    # Assuming you want to redirect back to the contact page after submitting
    return redirect('/contact')

@app.route('/faqs')
def faqs():
    # Add your code to render the faq.html page
    return render_template('faq.html')

@app.route('/submit_faq', methods=['POST'])
def submit_faq():
    # Retrieve the submitted form data
    question1 = request.form['question1']
    answer1 = request.form['answer1']
    question2 = request.form['question2']
    answer2 = request.form['answer2']
    # Add more questions and answers as needed

    # Add any necessary logic or data processing here

    # Assuming you want to redirect back to the FAQ page after submitting
    return redirect('/faq')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/vegan-menu')
def vegan_menu():
    # Get the search query parameter from the URL
    search_query = request.args.get('search')

    # Get the full inventory from the database
    full_inventory = db.get_full_inventory()

    # Filter out the vegan items
    vegan_items = [item for item in full_inventory if item['is_vegan']]

    # Filter the vegan items based on the search query
    if search_query:
        vegan_items = [item for item in vegan_items if search_query.lower() in item['item_name'].lower()]

    return render_template('vegan_menu.html', vegan_items=vegan_items)

@app.route('/')
def index():
    # Get the search query parameter from the URL
    search_query = request.args.get('search')

    # Get the full inventory from the database
    full_inventory = db.get_full_inventory()

    # Filter the inventory based on the search query
    if search_query:
        products = [item for item in full_inventory if search_query.lower() in item['item_name'].lower()]
    else:
        products = full_inventory

    return render_template('index.html', products=products)

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search')

    # Get the full inventory from the database
    full_inventory = db.get_full_inventory()

    # Filter the products based on the search query
    search_results = [product for product in full_inventory if search_query.lower() in product['item_name'].lower()]

    return render_template('index.html', products=search_results)

@app.route('/process_order', methods=['POST'])
def process_order():
    """
    Process the user's order and show the confirmation page.

    Args:
        - None

    Returns:
        - render_template: Renders the confirmation page.

    Modifies:
        - None
    """
    # Perform any necessary order processing here (e.g., payment processing, order confirmation, etc.)
    # After processing the order, you can redirect the user to the confirmation page or render it directly.

    return render_template('confirmation.html')

@app.route('/checkout/success')
def confirmation():
    return render_template('checkout.html')


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
