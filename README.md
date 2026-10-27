# Banking Transaction Analysis System

A Flask web application backed by MySQL that stores customers, accounts and transactions (synthetic data only), exposes them through a REST-style API, and visualises deposits vs. withdrawals using Pandas and Matplotlib. It includes a single-page admin dashboard for viewing data, adding customers/transactions, and removing customers.

> **Python Group Project 16** – Banking Transaction Analysis System

---

## Features

- **Dashboard overview** – the 10 most recent transactions, joined across customers, accounts and transactions
- **Analytics & graphs** – auto-generated charts:
  - Total deposits vs. withdrawals (all customers)
  - Deposits vs. withdrawals per customer
- **Data views** – browse customers, accounts and all transactions
- **Add customer** – creates a customer and a linked account in one step
- **Add transaction** – records a deposit or withdrawal against an account
- **Remove customer** – deletes a customer, their accounts and all their transactions by account ID
- **Auto-refresh charts** – charts are regenerated after every add/remove action

---

## Tech Stack

| Layer        | Technology                      |
|--------------|---------------------------------|
| Backend      | Python 3, Flask                 |
| Database     | MySQL (`mysql-connector-python`)|
| Analysis     | Pandas                          |
| Visualisation| Matplotlib (`Agg` backend)      |
| Frontend     | HTML, CSS, vanilla JavaScript (Jinja2 template) |

---

## Project Structure

```
.
├── web.py                  # Main Flask app (full dashboard, charts, add/delete endpoints)
├── app.py                  # Earlier, simpler API-only version (no charts/dashboard)
├── config.py               # MySQL connection helper
├── db_setup.py             # Database connection / schema and sample-data setup (schema is commented out)
├── templates/
│   └── index.html          # Dashboard UI (must live in a `templates/` folder)
└── static/
    ├── transaction_chart.png           # Generated: deposits vs withdrawals
    └── customer_transaction_chart.png  # Generated: per-customer breakdown
```

> Flask's `render_template` looks for `index.html` inside a `templates/` folder, and charts are saved to `static/`. Create these folders if they don't exist.

---

## Database Schema

Database name: `bank_details`

```sql
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type ENUM('SAVINGS', 'CURRENT') NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type ENUM('DEPOSIT', 'WITHDRAWAL') NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    description_optional VARCHAR(120) NULL,
    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
```

The `amount > 0` check constraint and the `ENUM` types keep transaction data valid at the database level.

---

## Getting Started

### 1. Prerequisites

- Python 3.9+
- MySQL Server running locally

### 2. Install dependencies

```bash
pip install flask mysql-connector-python pandas matplotlib
```

### 3. Create the database

```sql
CREATE DATABASE bank_details;
USE bank_details;
-- then run the schema above
```

Optionally insert sample customers, accounts and transactions (synthetic data only).

### 4. Configure the connection

Edit `config.py` with your MySQL credentials:

```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="<your-password>",
    database="bank_details"
)
```

> **Security note:** don't commit real passwords to Git. Prefer environment variables (e.g. `os.getenv("DB_PASSWORD")`) or a `.env` file listed in `.gitignore`.

### 5. Run the app

```bash
python web.py
```

Open <http://127.0.0.1:5000/dashboard> in your browser.

---

## API Endpoints

| Method | Endpoint                    | Description                                              |
|--------|-----------------------------|----------------------------------------------------------|
| GET    | `/`                         | Welcome message                                          |
| GET    | `/dashboard`                | Dashboard UI with the 10 latest transactions             |
| GET    | `/customers`                | List all customers                                       |
| POST   | `/customers`                | Add a customer + account                                 |
| GET    | `/customers/accounts`       | List all accounts                                        |
| GET    | `/customers/transactions`   | Customer/account/transaction join view                   |
| POST   | `/transactions`             | Add a new transaction                                    |
| POST   | `/customers/delete-by-account` | Delete a customer, accounts and transactions by `account_id` |
| GET    | `/generate-chart`           | Generate the deposits vs. withdrawals chart              |
| GET    | `/generate-customer-chart`  | Generate the per-customer chart                          |

### Example requests

**Add a customer**
```bash
curl -X POST http://127.0.0.1:5000/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "Anil", "account_type": "SAVINGS"}'
```

**Add a transaction**
```bash
curl -X POST http://127.0.0.1:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{
        "account_id": 1,
        "transaction_date": "2026-02-01",
        "transaction_type": "DEPOSIT",
        "amount": 2500.00,
        "description": "Salary credit"
      }'
```

**Delete a customer by account ID**
```bash
curl -X POST http://127.0.0.1:5000/customers/delete-by-account \
  -H "Content-Type: application/json" \
  -d '{"account_id": 3}'
```

---

## Sample Output

**Total deposits vs. withdrawals** – deposits significantly exceed withdrawals across the dataset.

![Total deposits vs withdrawals](static/transaction_chart.png)

**Deposits vs. withdrawals per customer** – shows each customer's activity side by side (e.g. `shanmukh` has the highest deposit total, while `Hemanth` is the only customer with withdrawals above deposits).

![Per-customer transactions](static/customer_transaction_chart.png)

---

## How It Works

1. `config.connect()` opens a MySQL connection for each request.
2. Flask routes query the database with SQL joins across `customers`, `accounts` and `transactions`.
3. Pandas aggregates the data (`groupby` / `pivot_table`) and Matplotlib saves bar charts to `static/`.
4. The dashboard (`index.html`) fetches data from the API using JavaScript, and refreshes charts after every change.

---

## Notes & Known Limitations

- `app.py` is an earlier version of the API; **`web.py` is the main application** to run.
- All data is synthetic – this project is for learning and demonstration only.
- There is no authentication yet; the delete endpoint is unprotected.
- Chart labels use `$` as the currency symbol.
- `config.py` prints the connection object on import; remove `print(connect())` for cleaner startup.

## Future Enhancements

- Rule-based flagging of unusual transactions (e.g. very large withdrawals)
- Basic access control / login for admin actions
- Account balance tracking and monthly summary reports
- Environment-based configuration for credentials

---

## Authors

Python Group Project 16 team.
