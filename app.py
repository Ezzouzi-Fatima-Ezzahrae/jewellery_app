from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'database.db'

# Helper function to get a database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Product detail route
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cur.fetchone()
    conn.close()
    return render_template('product_detail.html', product=product)

# Cart route
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# Add to cart route
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cur.fetchone()
    
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append({'id': product['id'], 'name': product['name'], 'price': product['price']})
    session.modified = True
    return redirect(url_for('index'))

# Admin panel route
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_url = request.form['image_url']
        cur.execute("INSERT INTO products (name, price, description, image_url) VALUES (?, ?, ?, ?)",
                    (name, price, description, image_url))
        conn.commit()
        return redirect(url_for('admin'))

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return render_template('admin.html', products=products)

# Delete product
@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


# Create the database and products table
conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS products
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                description TEXT,
                image_url TEXT)''')

# Sample data
sample_products = [
    ('Stainless Steel Ring', 29.99, 'Elegant stainless steel ring.', 'url_to_your_image'),
    ('Stainless Steel Necklace', 49.99, 'Stylish stainless steel necklace.', 'url_to_your_image'),
    ('Stainless Steel Bracelet', 19.99, 'Durable stainless steel bracelet.', 'url_to_your_image')
]

cur.executemany("INSERT INTO products (name, price, description, image_url) VALUES (?, ?, ?, ?)",
                sample_products)

conn.commit()
conn.close()

if __name__ == '__main__':
    app.run(debug=True)
