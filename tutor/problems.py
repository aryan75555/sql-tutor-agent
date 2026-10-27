PROBLEMS = [
    {
        "id": 1,
        "title": "High earners",
        "difficulty": "Easy",
        "topic": "WHERE",
        "description": "Show the name and salary of every employee whose salary is greater than 60000.",
        "solution": "SELECT name, salary FROM employees WHERE salary > 60000",
        "ordered": False,
        "hints": [
            "You only want some of the rows from one table. Which clause filters rows?",
            "Filter the salary column using a comparison operator.",
            "Pick two columns from the employees table and keep only rows where salary is above the given number.",
        ],
    },
    {
        "id": 2,
        "title": "Delhi customers",
        "difficulty": "Easy",
        "topic": "WHERE, ORDER BY",
        "description": "Show the name and city of customers who live in Delhi, sorted by name from A to Z.",
        "solution": "SELECT name, city FROM customers WHERE city = 'Delhi' ORDER BY name",
        "ordered": True,
        "hints": [
            "Two things are needed here: filtering rows and sorting them.",
            "Text values in a filter need quotes. Sorting is done with a clause that comes after the filter.",
            "Filter customers by city, then sort the result by name in ascending order.",
        ],
    },
    {
        "id": 3,
        "title": "Top three earners",
        "difficulty": "Easy",
        "topic": "ORDER BY, LIMIT",
        "description": "Show the name and salary of the three highest paid employees, highest salary first.",
        "solution": "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3",
        "ordered": True,
        "hints": [
            "Think about sorting first, then about cutting the result short.",
            "Sort by salary in descending order, then restrict how many rows come back.",
            "Order the employees by salary from high to low and keep only the first three rows.",
        ],
    },
    {
        "id": 4,
        "title": "Employees with departments",
        "difficulty": "Medium",
        "topic": "JOIN",
        "description": "List each employee's name together with the name of their department (employee name first, department name second).",
        "solution": "SELECT e.name, d.name FROM employees e JOIN departments d ON e.department_id = d.id",
        "ordered": False,
        "hints": [
            "The data you need lives in two different tables.",
            "Combine employees and departments by matching the department id stored in employees to the id in departments.",
            "Use an inner join between the two tables on the department id relationship, then select the two names.",
        ],
    },
    {
        "id": 5,
        "title": "Headcount per department",
        "difficulty": "Medium",
        "topic": "LEFT JOIN, GROUP BY",
        "description": "For every department, show the department name and the number of employees in it. Departments with no employees must also appear with a count of 0.",
        "solution": "SELECT d.name, COUNT(e.id) FROM departments d LEFT JOIN employees e ON e.department_id = d.id GROUP BY d.name",
        "ordered": False,
        "hints": [
            "Look at the departments table closely. Is there a department that would disappear with a normal join?",
            "You need a join type that keeps every row from the left table, and then grouping to count per department.",
            "Start from departments, keep unmatched rows when joining to employees, group by department name, and count a column from employees rather than counting all rows.",
        ],
    },
    {
        "id": 6,
        "title": "Delivered revenue per customer",
        "difficulty": "Medium",
        "topic": "JOIN, WHERE, GROUP BY, SUM",
        "description": "Show each customer's name and the total amount of their orders with status 'Delivered'. Only include customers who have at least one delivered order.",
        "solution": "SELECT c.name, SUM(o.amount) FROM customers c JOIN orders o ON o.customer_id = c.id WHERE o.status = 'Delivered' GROUP BY c.name",
        "ordered": False,
        "hints": [
            "You need data from customers and orders, and one total per customer.",
            "Filter the orders by status before grouping, and use an aggregate function on the amount column.",
            "Join customers to orders, keep only delivered rows with WHERE, group by customer name, and add up the amounts.",
        ],
    },
    {
        "id": 7,
        "title": "Well paid departments",
        "difficulty": "Medium",
        "topic": "GROUP BY, HAVING",
        "description": "Show the department name and average salary for departments whose average salary is above 60000.",
        "solution": "SELECT d.name, AVG(e.salary) FROM departments d JOIN employees e ON e.department_id = d.id GROUP BY d.name HAVING AVG(e.salary) > 60000",
        "ordered": False,
        "hints": [
            "The condition is on a group, not on a single row.",
            "WHERE cannot filter on an aggregate result. There is another clause meant for that.",
            "Join the two tables, group by department name, compute the average salary, and filter the groups after grouping.",
        ],
    },
    {
        "id": 8,
        "title": "Above company average",
        "difficulty": "Hard",
        "topic": "Subquery",
        "description": "Show the name and salary of employees who earn more than the average salary of all employees.",
        "solution": "SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)",
        "ordered": False,
        "hints": [
            "You must compare each salary against a single number that you first have to calculate.",
            "A query can be placed inside another query's filter condition.",
            "Write a small query that returns the average salary, and use it inside the filter condition of the main query.",
        ],
    },
    {
        "id": 9,
        "title": "Customers without orders",
        "difficulty": "Hard",
        "topic": "Subquery, NOT IN",
        "description": "Show the names of customers who have never placed an order.",
        "solution": "SELECT name FROM customers WHERE id NOT IN (SELECT customer_id FROM orders)",
        "ordered": False,
        "hints": [
            "You are looking for rows in one table that have no matching rows in another table.",
            "Either a subquery with a negative membership check, or a join that keeps unmatched rows, can solve this.",
            "Select customer names whose id does not appear among the customer ids of the orders table.",
        ],
    },
    {
        "id": 10,
        "title": "Earning more than the manager",
        "difficulty": "Hard",
        "topic": "Self JOIN",
        "description": "Show the employee name and the manager name for employees who earn more than their own manager (employee name first, manager name second).",
        "solution": "SELECT e.name, m.name FROM employees e JOIN employees m ON e.manager_id = m.id WHERE e.salary > m.salary",
        "ordered": False,
        "hints": [
            "Employees and managers are stored in the same table.",
            "Use the same table twice with different aliases, linked through the manager id column.",
            "Join employees to itself where one side's manager id equals the other side's id, then compare the two salaries.",
        ],
    },
]


def get_problem(problem_id):
    for problem in PROBLEMS:
        if problem["id"] == problem_id:
            return problem
    raise KeyError(problem_id)
