use restaurant_management;

INSERT INTO Categories(category_name)
VALUES
('Pizza'),
('Burger'),
('Pasta'),
('Beverages'),
('Desserts');

INSERT INTO Menu_Items (item_name, price, category_id)
VALUES
('Margherita Pizza', 299.00, 1),
('Farmhouse Pizza', 399.00, 1),
('Paneer Tikka Pizza', 449.00, 1),

('Veg Burger', 149.00, 2),
('Cheese Burger', 199.00, 2),
('Paneer Burger', 179.00, 2),

('White Sauce Pasta', 249.00, 3),
('Red Sauce Pasta', 229.00, 3),
('Cheese Pasta', 279.00, 3),

('Cold Coffee', 99.00, 4),
('Chocolate Shake', 129.00, 4),
('Mango Smoothie', 119.00, 4),

('Brownie', 99.00, 5),
('Vanilla Ice Cream', 79.00, 5),
('Chocolate Cake', 149.00, 5);

INSERT INTO Restaurant_Tables (table_number, qr_code)
VALUES
(1,'QR001'),
(2,'QR002'),
(3,'QR003'),
(4,'QR004'),
(5,'QR005'),
(6,'QR006'),
(7,'QR007'),
(8,'QR008'),
(9,'QR009'),
(10,'QR010');
