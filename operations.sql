-- 1. Display all customers with their orders.
SELECT 
    c.customer_name, o.order_id, o.order_date
FROM
    Customers c
        INNER JOIN
    Orders o ON c.customer_id = o.customer_id;

-- 2. Show customer name, table number, and order status.
SELECT 
    c.customer_name, rt.table_number, o.order_status
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Restaurant_Tables rt ON o.table_id = rt.table_id;
    
-- 3. Display ordered food items with customer names.
SELECT 
    c.customer_name, m.item_name, od.quantity
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Order_details od ON o.order_id = od.order_id
        JOIN
    Menu_Items m ON od.item_id = m.item_id;
    
-- 4. Show payment details with customer names.
SELECT 
    c.customer_name,
    p.amount,
    p.payment_method,
    p.payment_status
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Payments p ON o.order_id = p.order_id;

-- 5. Display all menu items with their category.
SELECT 
    c.category_name, m.item_name, m.price
FROM
    Menu_Items m
        JOIN
    Categories c ON c.category_id = m.category_id;
    
-- 6. Show complete bill details.
SELECT 
    c.customer_name,
    m.item_name,
    od.quantity,
    od.subtotal,
    p.payment_method
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Order_Details od ON o.order_id = od.order_id
        JOIN
    Menu_Items m ON od.item_id = m.item_id
        JOIN
    Payments p ON o.order_id = p.order_id;

-- 7. Find all pending orders.
SELECT 
    c.customer_name, o.order_status
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
WHERE
    o.order_status = 'pending';
    
-- 8. Show all completed payments.
SELECT 
    c.customer_name, o.order_id, p.payment_status
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Payments p ON o.order_id = p.payment_id
WHERE
    o.order_status = 'completed';

-- 9. Find total sales.
SELECT 
    SUM(amount) AS total_sale
FROM
    Payments
WHERE
    payment_status = 'completed';

-- 10. Find average order amount.
SELECT 
    AVG(amount) AS avg_amount
FROM
    Payments;

-- 11. Find highest payment.
SELECT 
    MAX(amount) AS max_amount
FROM
    Payments;

-- 12. Find lowest payment.
SELECT 
    MIN(amount) AS min_amount
FROM
    Payments;

-- 13. Count total customers.
SELECT 
    COUNT(*) AS total_customer
FROM
    Customers;

-- 14. Count total orders.
SELECT 
    COUNT(*) AS total_order
FROM
    Orders;

-- 15. Find most expensive menu item.
SELECT 
    item_name, price
FROM
    Menu_Items
ORDER BY price DESC
LIMIT 1;

-- 16. Find cheapest menu item.
SELECT 
    item_name, price
FROM
    Menu_Items
ORDER BY price ASC
LIMIT 1;

-- 17. Display items ordered more than once.
SELECT 
    item_id, SUM(quantity) AS Total_Quantity
FROM
    Order_Details
GROUP BY item_id
HAVING SUM(quantity) > 1;

-- 18. Find total quantity sold for each item.
SELECT 
    m.item_name, SUM(od.quantity) AS total_sold
FROM
    Menu_Items m
        JOIN
    Order_Details od ON m.item_id = od.item_id
GROUP BY m.item_name;

-- 19. Show total revenue for each menu item.
SELECT 
    m.item_name, SUM(od.subtotal) AS revenue
FROM
    Menu_Items m
        JOIN
    Order_Details od ON m.item_id = od.item_id
GROUP BY m.item_name;

-- 20. Show number of orders for each customer.
SELECT 
    c.customer_name, COUNT(o.order_id) AS Total_Orders
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name;

-- 21. Display orders with table number.
SELECT 
    o.order_id, t.table_number
FROM
    Orders o
        JOIN
    Restaurant_Tables t ON o.table_id = t.table_id;

-- 22. Find customers who paid using UPI.
SELECT 
    c.customer_name, p.payment_method
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Payments p ON o.order_id = p.order_id
WHERE
    p.payment_method = 'UPI';
    
-- 23. Find customers who paid by Card.
SELECT 
    c.customer_name, p.payment_method
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Payments p ON o.order_id = p.order_id
WHERE
    p.payment_method = 'Card';

-- 24. Display all menu items sorted by price.
SELECT 
    m.item_id, m.item_name, m.price
FROM
    Menu_Items m
ORDER BY m.price DESC;

-- 25. Find category-wise menu count.
SELECT 
    c.category_name, COUNT(m.item_id) AS total_items
FROM
    Categories c
        JOIN
    Menu_Items m ON c.category_id = m.category_id
GROUP BY c.category_name;

-- 26. Display customer, food item, quantity, amount, and payment method.
SELECT 
    c.customer_name,
    m.item_name,
    od.quantity,
    p.amount,
    p.payment_method
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Order_Details od ON od.order_id = o.order_id
        JOIN
    Menu_Items m ON m.item_id = od.item_id
        JOIN
    Payments p ON p.order_id = p.order_id;
    
-- 27. Show the total bill for each customer.
SELECT 
    c.customer_name, SUM(od.subtotal) AS total_bill
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Order_Details od ON od.order_id = o.order_id
GROUP BY c.customer_name;

-- 28. Find the top 5 customers based on bill amount.
SELECT 
    c.customer_name, SUM(od.subtotal) AS total_bill
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Order_Details od ON od.order_id = o.order_id
GROUP BY c.customer_name
ORDER BY total_bill DESC
LIMIT 5;

-- 29. Find the most ordered menu item.
SELECT 
    m.item_name, SUM(od.quantity) AS total_ordered
FROM
    Menu_Items m
        JOIN
    Order_Details od ON od.item_id = m.item_id
GROUP BY m.item_name
ORDER BY total_ordered DESC
LIMIT 1;

-- 30. Display complete restaurant report.
SELECT 
    c.customer_name,
    rt.table_number,
    m.item_name,
    od.quantity,
    od.subtotal,
    p.payment_method,
    o.order_status
FROM
    Customers c
        JOIN
    Orders o ON c.customer_id = o.customer_id
        JOIN
    Restaurant_Tables rt ON o.table_id = rt.table_id
        JOIN
    Order_Details od ON o.order_id = od.order_id
        JOIN
    Menu_Items m ON od.item_id = m.item_id
        JOIN
    Payments p ON o.order_id = p.order_id;
