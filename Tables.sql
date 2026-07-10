use restaurant_management;

CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50)
);
select *from Categories;

CREATE TABLE Menu_Items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(100),
    price DECIMAL(10,2),
    category_id INT,
    FOREIGN KEY(category_id)
    REFERENCES Categories(category_id)
);
select *from Menu_Items;

CREATE TABLE Restaurant_Tables (
    table_id INT PRIMARY KEY AUTO_INCREMENT,
    table_number INT,
    qr_code VARCHAR(255)
);
select *from Restaurant_Tables;

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100),
    phone_no VARCHAR(15)
);
select * from Customers;

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    table_id INT,
    order_date DATETIME,
    order_status VARCHAR(30),
    FOREIGN KEY(customer_id)
    REFERENCES Customers(customer_id),
    FOREIGN KEY(table_id)
    REFERENCES Restaurant_Tables(table_id)
);
select *from Orders;

CREATE TABLE Order_Details (
    order_detail_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    item_id INT,
    quantity INT,
    subtotal DECIMAL(10,2),
    FOREIGN KEY(order_id)
    REFERENCES Orders(order_id),
    FOREIGN KEY(item_id)
    REFERENCES Menu_Items(item_id)
);
select *from Order_Details;

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    amount DECIMAL(10,2),
    payment_method VARCHAR(30),
    payment_status VARCHAR(30),
    FOREIGN KEY(order_id)
    REFERENCES Orders(order_id)
);
select *from Payments;
