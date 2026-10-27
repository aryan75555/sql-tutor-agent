CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    salary INTEGER NOT NULL,
    hire_date TEXT NOT NULL,
    manager_id INTEGER REFERENCES employees(id)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date TEXT NOT NULL,
    amount INTEGER NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO departments VALUES
(1, 'Engineering', 'Bengaluru'),
(2, 'Sales', 'Mumbai'),
(3, 'Marketing', 'Delhi'),
(4, 'Legal', 'Delhi');

INSERT INTO employees VALUES
(1, 'Aarav Sharma', 1, 90000, '2019-03-15', NULL),
(2, 'Priya Singh', 1, 75000, '2020-07-01', 1),
(3, 'Rohan Mehta', 1, 55000, '2021-01-10', 1),
(4, 'Sneha Iyer', 1, 95000, '2018-05-20', 1),
(5, 'Vikram Rao', 2, 60000, '2019-11-05', NULL),
(6, 'Anjali Gupta', 2, 45000, '2022-02-14', 5),
(7, 'Karan Malhotra', 2, 48000, '2021-09-30', 5),
(8, 'Neha Verma', 3, 62000, '2020-04-18', NULL),
(9, 'Rahul Khanna', 3, 52000, '2022-08-22', 8),
(10, 'Pooja Nair', 3, 70000, '2019-12-01', 8),
(11, 'Arjun Das', 1, 65000, '2023-01-09', 1),
(12, 'Meera Joshi', 2, 58000, '2023-06-12', 5);

INSERT INTO customers VALUES
(1, 'Amit Kumar', 'Delhi'),
(2, 'Ritu Sharma', 'Mumbai'),
(3, 'Sanjay Patel', 'Delhi'),
(4, 'Divya Reddy', 'Hyderabad'),
(5, 'Manish Jain', 'Mumbai'),
(6, 'Kavita Roy', 'Delhi'),
(7, 'Farhan Ali', 'Hyderabad');

INSERT INTO orders VALUES
(1, 1, '2024-01-05', 1200, 'Delivered'),
(2, 1, '2024-02-11', 800, 'Delivered'),
(3, 2, '2024-02-15', 1500, 'Shipped'),
(4, 2, '2024-03-02', 700, 'Delivered'),
(5, 3, '2024-03-10', 2200, 'Delivered'),
(6, 3, '2024-03-25', 300, 'Cancelled'),
(7, 4, '2024-04-01', 950, 'Delivered'),
(8, 4, '2024-04-12', 1100, 'Pending'),
(9, 5, '2024-04-20', 400, 'Delivered'),
(10, 5, '2024-05-03', 1800, 'Delivered'),
(11, 1, '2024-05-14', 600, 'Cancelled'),
(12, 2, '2024-05-21', 2500, 'Delivered'),
(13, 4, '2024-06-02', 350, 'Delivered'),
(14, 3, '2024-06-15', 1250, 'Pending');
