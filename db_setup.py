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
# bulk_transactions = [
#     (1, '2026-02-11', 'DEPOSIT', 1500.00, 'ATM cash deposit'),
#     (2, '2026-02-11', 'WITHDRAWAL', 450.00, 'Supermarket'),
#     (3, '2026-02-12', 'DEPOSIT', 3200.00, 'Freelance work'),
#     (4, '2026-02-12', 'WITHDRAWAL', 120.00, 'Coffee shop'),
#     (5, '2026-02-13', 'DEPOSIT', 12000.00, 'Monthly salary'),
#     (6, '2026-02-13', 'WITHDRAWAL', 2500.00, 'Utility bill'),
#     (7, '2026-02-14', 'DEPOSIT', 450.00, 'Friend transfer'),
#     (8, '2026-02-14', 'WITHDRAWAL', 1500.00, 'Shopping mall'),
#     (9, '2026-02-15', 'DEPOSIT', 8500.00, 'Consulting fee'),
#     (10, '2026-02-15', 'WITHDRAWAL', 300.00, 'Fuel station'),
#     (1, '2026-02-16', 'WITHDRAWAL', 800.00, 'Restaurant'),
#     (2, '2026-02-16', 'DEPOSIT', 2100.00, 'Cashback reward'),
#     (3, '2026-02-17', 'WITHDRAWAL', 150.00, 'Bookstore'),
#     (4, '2026-02-17', 'DEPOSIT', 5000.00, 'Web design project'),
#     (5, '2026-02-18', 'WITHDRAWAL', 3200.00, 'Rent payment'),
#     (6, '2026-02-18', 'DEPOSIT', 450.00, 'Refund'),
#     (7, '2026-02-19', 'WITHDRAWAL', 900.00, 'Electronics store'),
#     (8, '2026-02-19', 'DEPOSIT', 3500.00, 'Dividend'),
#     (9, '2026-02-20', 'WITHDRAWAL', 1100.00, 'Doctor consultation'),
#     (10, '2026-02-20', 'DEPOSIT', 6000.00, 'Bonus payout'),
#     (1, '2026-02-21', 'DEPOSIT', 1250.00, 'Sales commission'),
#     (2, '2026-02-21', 'WITHDRAWAL', 500.00, 'Cinema tickets'),
#     (3, '2026-02-22', 'DEPOSIT', 4100.00, 'Design contract'),
#     (4, '2026-02-22', 'WITHDRAWAL', 230.00, 'Pharmacy'),
#     (5, '2026-02-23', 'DEPOSIT', 15000.00, 'Client advance'),
#     (6, '2026-02-23', 'WITHDRAWAL', 1200.00, 'Internet bill'),
#     (7, '2026-02-24', 'DEPOSIT', 950.00, 'Peer transfer'),
#     (8, '2026-02-24', 'WITHDRAWAL', 670.00, 'Clothing store'),
#     (9, '2026-02-25', 'DEPOSIT', 7200.00, 'Project closure'),
#     (10, '2026-02-25', 'WITHDRAWAL', 450.00, 'Car wash'),
#     (1, '2026-02-26', 'WITHDRAWAL', 1500.00, 'Hotel booking'),
#     (2, '2026-02-26', 'DEPOSIT', 3300.00, 'Affiliate payout'),
#     (3, '2026-02-27', 'WITHDRAWAL', 85.00, 'Bakery'),
#     (4, '2026-02-27', 'DEPOSIT', 6200.00, 'Consultancy'),
#     (5, '2026-02-28', 'WITHDRAWAL', 4000.00, 'Mortgage payment'),
#     (6, '2026-02-28', 'DEPOSIT', 1200.00, 'Tax refund'),
#     (7, '2026-03-01', 'WITHDRAWAL', 550.00, 'Gym membership'),
#     (8, '2026-03-01', 'DEPOSIT', 4500.00, 'Stock sale'),
#     (9, '2026-03-02', 'WITHDRAWAL', 1290.00, 'Insurance premium'),
#     (10, '2026-03-02', 'DEPOSIT', 8000.00, 'Quarterly bonus'),
#     (1, '2026-03-03', 'DEPOSIT', 2200.00, 'Part-time payment'),
#     (2, '2026-03-03', 'WITHDRAWAL', 340.00, 'Fast food'),
#     (3, '2026-03-04', 'DEPOSIT', 3900.00, 'Editorial fee'),
#     (4, '2026-03-04', 'WITHDRAWAL', 180.00, 'Stationery'),
#     (5, '2026-03-05', 'DEPOSIT', 14000.00, 'Salary'),
#     (6, '2026-03-05', 'WITHDRAWAL', 2100.00, 'Electricity bill'),
#     (7, '2026-03-06', 'DEPOSIT', 850.00, 'Gift card cashout'),
#     (8, '2026-03-06', 'WITHDRAWAL', 950.00, 'Hardware store'),
#     (9, '2026-03-07', 'DEPOSIT', 5100.00, 'Ad revenue'),
#     (10, '2026-03-07', 'WITHDRAWAL', 600.00, 'Maintenance fee'),
#     (1, '2026-03-08', 'WITHDRAWAL', 700.00, 'Pub night'),
#     (2, '2026-03-08', 'DEPOSIT', 1800.00, 'Reimbursement'),
#     (3, '2026-03-09', 'WITHDRAWAL', 420.00, 'Pet supplies'),
#     (4, '2026-03-09', 'DEPOSIT', 4800.00, 'Writing contract'),
#     (5, '2026-03-10', 'WITHDRAWAL', 3500.00, 'Rent'),
#     (6, '2026-03-10', 'DEPOSIT', 900.00, 'Cash deposit'),
#     (7, '2026-03-11', 'WITHDRAWAL', 1300.00, 'Flight booking'),
#     (8, '2026-03-11', 'DEPOSIT', 3100.00, 'Dividend payout'),
#     (9, '2026-03-12', 'WITHDRAWAL', 750.00, 'Dental checkup'),
#     (10, '2026-03-12', 'DEPOSIT', 5500.00, 'Project bonus'),
#     (1, '2026-03-13', 'DEPOSIT', 1950.00, 'Service charge'),
#     (2, '2026-03-13', 'WITHDRAWAL', 290.00, 'Music streaming'),
#     (3, '2026-03-14', 'DEPOSIT', 3600.00, 'Translation work'),
#     (4, '2026-03-14', 'WITHDRAWAL', 310.00, 'Cloud hosting'),
#     (5, '2026-03-15', 'DEPOSIT', 13500.00, 'Client deposit'),
#     (6, '2026-03-15', 'WITHDRAWAL', 1150.00, 'Water bill'),
#     (7, '2026-03-16', 'DEPOSIT', 1200.00, 'Sibling transfer'),
#     (8, '2026-03-16', 'WITHDRAWAL', 840.00, 'Home decor'),
#     (9, '2026-03-17', 'DEPOSIT', 6400.00, 'Milestone payment'),
#     (10, '2026-03-17', 'WITHDRAWAL', 520.00, 'Car insurance'),
#     (1, '2026-03-18', 'WITHDRAWAL', 2200.00, 'Laptop repair'),
#     (2, '2026-03-18', 'DEPOSIT', 2900.00, 'Referral bonus'),
#     (3, '2026-03-19', 'WITHDRAWAL', 140.00, 'Snacks'),
#     (4, '2026-03-19', 'DEPOSIT', 5700.00, 'App development'),
#     (5, '2026-03-20', 'WITHDRAWAL', 3800.00, 'Mortgage'),
#     (6, '2026-03-20', 'DEPOSIT', 1100.00, 'Tax credit'),
#     (7, '2026-03-21', 'WITHDRAWAL', 480.00, 'Yoga classes'),
#     (8, '2026-03-21', 'DEPOSIT', 3900.00, 'Bond interest'),
#     (9, '2026-03-22', 'WITHDRAWAL', 1500.00, 'Medical tests'),
#     (10, '2026-03-22', 'DEPOSIT', 7500.00, 'Incentive'),
#     (1, '2026-03-23', 'DEPOSIT', 2500.00, 'Freelance task'),
#     (2, '2026-03-23', 'WITHDRAWAL', 410.00, 'Pizza delivery'),
#     (3, '2026-03-24', 'DEPOSIT', 3400.00, 'Logo design'),
#     (4, '2026-03-24', 'WITHDRAWAL', 220.00, 'Domain renewal'),
#     (5, '2026-03-25', 'DEPOSIT', 16000.00, 'Monthly salary'),
#     (6, '2026-03-25', 'WITHDRAWAL', 1900.00, 'Gas bill'),
#     (7, '2026-03-26', 'DEPOSIT', 920.00, 'Split bill refund'),
#     (8, '2026-03-26', 'WITHDRAWAL', 1100.00, 'Shoes purchase'),
#     (9, '2026-03-27', 'DEPOSIT', 6800.00, 'Contract completion'),
#     (10, '2026-03-27', 'WITHDRAWAL', 380.00, 'Car servicing'),
#     (1, '2026-03-28', 'WITHDRAWAL', 1800.00, 'Weekend trip'),
#     (2, '2026-03-28', 'DEPOSIT', 2700.00, 'Sale proceeds'),
#     (3, '2026-03-29', 'WITHDRAWAL', 95.00, 'Magazine subscription'),
#     (4, '2026-03-29', 'DEPOSIT', 5300.00, 'Consultancy fee'),
#     (5, '2026-03-30', 'WITHDRAWAL', 3600.00, 'Apartment rent'),
#     (6, '2026-03-30', 'DEPOSIT', 1450.00, 'Insurance claim'),
#     (7, '2026-03-31', 'WITHDRAWAL', 620.00, 'Sports equipment'),
#     (8, '2026-03-31', 'DEPOSIT', 4200.00, 'Stock dividend'),
#     (9, '2026-04-01', 'WITHDRAWAL', 1350.00, 'Health insurance'),
#     (10, '2026-04-01', 'DEPOSIT', 9000.00, 'Performance bonus')
# ]

# mycursor.executemany("""
#     INSERT INTO transactions (account_id, transaction_date, transaction_type, amount, description_optional)
#     VALUES (%s, %s, %s, %s, %s)
# """, bulk_transactions)
mycursor = mydb.cursor()

mydb.commit()
