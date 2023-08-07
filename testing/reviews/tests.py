# tests.py

# Import the app object from your main app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert b"Generic Cozy Restaurant" in response.data

def test_login_page():
    client = app.test_client()
    response = client.get('/login')
    assert b"Login" in response.data

def test_register_page():
    client = app.test_client()
    response = client.get('/register')
    assert b"Register" in response.data

def test_vegan_menu_page():
    client = app.test_client()
    response = client.get('/vegan-menu')
    assert b"Vegan Menu" in response.data

def test_checkout_page():
    client = app.test_client()
    response = client.get('/checkout')
    assert b"Your Order" in response.data
    assert b"Subtotal: $" in response.data
    assert b"Tax (7%): $" in response.data
    assert b"Grand Total: $" in response.data

def test_apply_discount():
    client = app.test_client()
    data = {
        'discount_code': 'tenoff'
    }
    response = client.post('/checkout', data=data, follow_redirects=True)
    assert b"Discount (tenoff): -$" in response.data

# Add more test functions for other routes and functionalities

if __name__ == '__main__':
    test_home_page()
    test_login_page()
    test_register_page()
    test_vegan_menu_page()
    test_checkout_page()
    test_apply_discount()
    # Call other test functions here
