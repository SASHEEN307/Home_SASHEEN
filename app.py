from flask import Flask, render_template, session, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sasheen_secret"

# =========================
# PRODUCTS
# =========================

products = {
    1: {
        "name": "Blue Crystal Bag",
        "price": 24,
        "img": "bluebag.jpg"
    },

    2: {
        "name": "Hot Pink Beaded Bag",
        "price": 18,
        "img": "pinkbag.jpg"
    },

    3: {
        "name": "Black Elegant Bag",
        "price": 30,
        "img": "blackbag.jpg"
    }
}

# =========================
# ORDERS DATABASE
# =========================

orders = []

# =========================
# HOME
# =========================

@app.route('/')
def home():
    return render_template('home.html')

# =========================
# SHOP
# =========================

@app.route('/shop')
def shop():
    return render_template(
        'shop.html',
        products=products
    )

# =========================
# ADD TO CART
# =========================

@app.route('/add/<int:id>')
def add_to_cart(id):

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(id)
    session.modified = True

    return redirect(url_for('cart'))

# =========================
# CART
# =========================

@app.route('/cart')
def cart():

    cart_items = []
    total = 0

    if 'cart' in session:

        for item_id in session['cart']:

            item = products[item_id]

            cart_items.append(item)

            total += item['price']

    return render_template(
        'cart.html',
        items=cart_items,
        total=total
    )

# =========================
# CLEAR CART
# =========================

@app.route('/clear')
def clear_cart():

    session['cart'] = []

    return redirect(url_for('cart'))

# =========================
# CHECKOUT
# =========================

@app.route('/checkout', methods=['POST'])
def checkout():

    if 'cart' not in session:
        return redirect(url_for('cart'))

    cart_items = []
    total = 0

    for item_id in session['cart']:

        item = products[item_id]

        cart_items.append(item)

        total += item['price']

    order = {
        "items": cart_items,
        "total": total,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    orders.append(order)

    session['cart'] = []

    return render_template(
        'success.html',
        order=order
    )

# =========================
# ORDERS DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    return render_template(
        'dashboard.html',
        orders=orders
    )

# =========================
# ABOUT
# =========================

@app.route('/about')
def about():
    return render_template('about.html')

# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)