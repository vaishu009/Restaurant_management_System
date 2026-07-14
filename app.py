from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from datetime import datetime
import random
import socket
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'restaurant_secret_key')

# Function to get local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# MySQL Configuration
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Vaishu@123'),
    'database': os.environ.get('DB_NAME', 'restaurant_management'),
    'port': int(os.environ.get('DB_PORT', '3306'))
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Helper function to get menu items
def fetch_menu_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT m.*, c.category_name 
        FROM Menu_Items m 
        JOIN Categories c ON m.category_id = c.category_id
    """
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

@app.route('/')
def index():
    # Generate a random table ID between 1 and 10
    random_table = random.randint(1, 10)
    
    # Use local IP address instead of localhost so phones on the same network can access it
    local_ip = get_local_ip()
    port = 5000
    menu_url = f"http://{local_ip}:{port}/menu?table_id={random_table}"
    
    # Generate a single QR code for this random table
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={menu_url}"
    
    return render_template('index.html', qr_code_url=qr_code_url, table_number=random_table, local_ip=local_ip)

@app.route('/tables')
def tables():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Restaurant_Tables")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Base URL for QR codes (using localhost for local testing)
    base_url = request.host_url.rstrip('/')
    for table in tables:
        # Generate the URL that the QR code will point to
        table['url'] = f"{base_url}/menu?table_id={table['table_id']}"
        # Use a public API to generate QR code image URL
        table['qr_image_url'] = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={table['url']}"
    
    return render_template('tables.html', tables=tables)

@app.route('/menu')
def menu():
    table_id = request.args.get('table_id')
    if table_id:
        session['table_id'] = table_id
    
    items = fetch_menu_items()
    # Group items by category
    categories = {}
    for item in items:
        cat = item['category_name']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    return render_template('menu.html', categories=categories)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    item_name = request.form.get('item_name')
    price = float(request.form.get('price'))
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    if item_id in cart:
        cart[item_id]['quantity'] += quantity
        cart[item_id]['subtotal'] = cart[item_id]['quantity'] * price
    else:
        cart[item_id] = {
            'item_id': item_id,
            'item_name': item_name,
            'price': price,
            'quantity': quantity,
            'subtotal': price * quantity
        }
    
    session['cart'] = cart
    return redirect(url_for('menu'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    total = sum(item['subtotal'] for item in cart_items.values())
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('menu'))

@app.route('/customer_details', methods=['GET', 'POST'])
def customer_details():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Insert customer and get ID
            cursor.execute("INSERT INTO Customers (customer_name, phone_no) VALUES (%s, %s)", (name, phone))
            conn.commit()
            customer_id = cursor.lastrowid
            session['customer_id'] = customer_id
            session['customer_name'] = name
            cursor.close()
            conn.close()
            print(f"DEBUG: Customer saved: {name}, ID: {customer_id}")
            return redirect(url_for('place_order'))
        except Exception as e:
            print(f"ERROR in customer_details: {e}")
            return f"Error saving customer: {e}", 500
    
    return render_template('customer.html')

@app.route('/place_order')
def place_order():
    if 'cart' not in session or 'customer_id' not in session:
        print("DEBUG: Missing cart or customer_id in session")
        return redirect(url_for('menu'))
    
    customer_id = session['customer_id']
    table_id = session.get('table_id', 1) 
    cart_items = session['cart']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create Order
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO Orders (customer_id, table_id, order_date, order_status) VALUES (%s, %s, %s, %s)",
            (customer_id, table_id, order_date, 'Pending')
        )
        order_id = cursor.lastrowid
        
        # Create Order Details
        total_amount = 0
        for item in cart_items.values():
            cursor.execute(
                "INSERT INTO Order_Details (order_id, item_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                (order_id, item['item_id'], item['quantity'], item['subtotal'])
            )
            total_amount += item['subtotal']
        
        conn.commit()
        session['order_id'] = order_id
        session['total_amount'] = total_amount
        cursor.close()
        conn.close()
        print(f"DEBUG: Order placed: ID {order_id}, Total: {total_amount}")
        return redirect(url_for('payment'))
    except Exception as e:
        print(f"ERROR in place_order: {e}")
        return f"Error placing order: {e}", 500

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        order_id = session.get('order_id')
        amount = session.get('total_amount')
        method = request.form.get('payment_method')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Payments (order_id, amount, payment_method, payment_status) VALUES (%s, %s, %s, %s)",
                (order_id, amount, method, 'Completed')
            )
            # Update order status
            cursor.execute("UPDATE Orders SET order_status = 'Completed' WHERE order_id = %s", (order_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            session['payment_method'] = method
            print(f"DEBUG: Payment saved for Order {order_id}, Method: {method}")
            return redirect(url_for('bill'))
        except Exception as e:
            print(f"ERROR in payment: {e}")
            return f"Error saving payment: {e}", 500
    
    return render_template('payment.html', amount=session.get('total_amount'))

@app.route('/bill')
def bill():
    order_id = session.get('order_id')
    if not order_id:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch order and customer details
    query = """
        SELECT o.order_id, c.customer_name, o.order_date, p.payment_method, p.amount
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        JOIN Payments p ON o.order_id = p.order_id
        WHERE o.order_id = %s
    """
    cursor.execute(query, (order_id,))
    order_info = cursor.fetchone()
    
    # Fetch ordered items
    query_items = """
        SELECT m.item_name, od.quantity, od.subtotal
        FROM Order_Details od
        JOIN Menu_Items m ON od.item_id = m.item_id
        WHERE od.order_id = %s
    """
    cursor.execute(query_items, (order_id,))
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Clear session after bill is generated
    session.pop('cart', None)
    
    return render_template('bill.html', order=order_info, items=items)

@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all orders
    cursor.execute("""
        SELECT o.order_id, c.customer_name, t.table_number, o.order_date, o.order_status, p.amount
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        JOIN Restaurant_Tables t ON o.table_id = t.table_id
        LEFT JOIN Payments p ON o.order_id = p.order_id
        ORDER BY o.order_date DESC
    """)
    orders = cursor.fetchall()
    
    # Total Sales
    cursor.execute("SELECT SUM(amount) as total_sales FROM Payments WHERE payment_status = 'Completed'")
    total_sales = cursor.fetchone()['total_sales'] or 0
    
    # Pending vs Completed
    cursor.execute("SELECT COUNT(*) as pending FROM Orders WHERE order_status = 'Pending'")
    pending_count = cursor.fetchone()['pending']
    
    cursor.execute("SELECT COUNT(*) as completed FROM Orders WHERE order_status = 'Completed'")
    completed_count = cursor.fetchone()['completed']
    
    cursor.close()
    conn.close()
    
    return render_template('admin.html', orders=orders, total_sales=total_sales, pending=pending_count, completed=completed_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
