import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aimlb2",
    database="bank_details"
)

# SCHEMA = """
# DROP TABLE IF EXISTS transactions;
# DROP TABLE IF EXISTS accounts;
# DROP TABLE IF EXISTS customers;
#
# CREATE TABLE customers (
#     customer_id INT AUTO_INCREMENT PRIMARY KEY,
#     name varchar(100) not null
# );
#
# CREATE TABLE accounts (
#     account_id INT AUTO_INCREMENT PRIMARY KEY,
#     customer_id INT NOT NULL,
#     account_type ENUM('SAVINGS', 'CURRENT') NOT NULL,
#     FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
# );
#
# CREATE TABLE transactions (
#     transaction_id INT AUTO_INCREMENT PRIMARY KEY,
#     account_id INT NOT NULL,
#     transaction_date DATE NOT NULL,
#     transaction_type ENUM('DEPOSIT', 'WITHDRAWAL') NOT NULL,
#     amount DECIMAL(12,2) NOT NULL,
#     description_optional VARCHAR(120) NULL,
#     CONSTRAINT chk_amount_positive CHECK (amount > 0),
#     FOREIGN KEY (account_id) REFERENCES accounts(account_id)
# );
# """
#

#
#
# for statement in SCHEMA.split(';'):
#     if statement.strip():
#         mycursor.execute(statement)
# customers=[
#     ("Ramu",),
#     ("Ravi",),
#     ("mahidhar",),
#     ("tharun",),
#     ("shanmukh",),
#     ("asif",),
#     ("Hemanth",),
#     ("Imran",),
#     ("Joshua",),
#     ("Ranga",)
# ]

# mycursor.executemany("INSERT INTO customers (name) VALUES (%s)", customers)
# transactions_data = [
#     (1, '2026-01-10', 'DEPOSIT', 5000.00, 'Initial deposit'),
#     (2, '2026-01-11', 'DEPOSIT', 12000.50, 'Salary credit'),
#     (3, '2026-01-12', 'WITHDRAWAL', 500.00, 'ATM withdrawal'),
#     (4, '2026-01-15', 'DEPOSIT', 3000.00, 'Freelance payment'),
#     (5, '2026-01-16', 'WITHDRAWAL', 1500.25, 'Grocery shopping'),
#     (6, '2026-01-18', 'DEPOSIT', 7500.00, 'Savings transfer'),
#     (7, '2026-01-20', 'WITHDRAWAL', 2000.00, 'Electricity bill'),
#     (8, '2026-01-22', 'DEPOSIT', 4500.00, 'Gift deposit'),
#     (9, '2026-01-24', 'WITHDRAWAL', 800.00, 'Restaurant payment'),
#     (10, '2026-01-25', 'DEPOSIT', 10000.00, 'Bonus credit')
# ]
#
# mycursor.executemany("""
#     INSERT INTO transactions (account_id, transaction_date, transaction_type, amount, description_optional)
#     VALUES (%s, %s, %s, %s, %s)
# """, transactions_data)
mycursor = mydb.cursor()

mydb.commit()
