# QR-Based Restaurant Management System

A complete web-based solution for restaurant management using Flask, MySQL, and Bootstrap 5.

## Features
- **Home Page**: Welcome screen for customers.
- **Menu Management**: Categorized menu items fetched from MySQL.
- **Cart System**: Session-based cart for ordering.
- **Customer Tracking**: Capture customer name and phone number.
- **Order Processing**: Create orders and order details in the database.
- **Payment Integration**: Multiple payment methods (UPI, Card, Cash).
- **Invoice Generation**: Clean, printable bill for customers.
- **Admin Dashboard**: Real-time sales data, order tracking, and statistics.
- **QR Support**: Table-specific menu links via `table_id` parameter.

## Prerequisites
- Python 3.x
- MySQL Server

## Setup Instructions

1. **Database Setup**:
   - Create a database named `restaurant_management`.
   - Run the SQL queries provided in `Tables.sql` to create the schema.
   - Run `insert_data.sql` to populate initial categories and menu items.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Open `app.py`.
   - Update the `db_config` dictionary with your MySQL credentials (username, password).

4. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000`.

## QR Code Usage
To simulate a table scan, use the following URL format:
`http://127.0.0.1:5000/menu?table_id=1`

## Project Structure
- `app.py`: Main Flask application logic.
- `templates/`: HTML files for frontend.
- `static/`: CSS and JS files.
- `requirements.txt`: Python package requirements.
