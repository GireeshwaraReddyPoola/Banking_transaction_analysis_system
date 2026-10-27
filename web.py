import os
import matplotlib
matplotlib.use('Agg')  # Prevents GUI crash on backend servers
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, jsonify, request, render_template
import config  # Imports database connection from config.py[cite: 2]

app = Flask(__name__)  # Initializes Flask application[cite: 4]

@app.route("/")
def hello_world():
    return "HELLO CUSTOMERS - BANKING TRANSACTION ANALYSIS SYSTEM"

# 1. Display all customers[cite: 4]
@app.route("/customers", methods=["GET"])
def customers():
    mydb = config.connect()  #[cite: 2, 4]
    mc = mydb.cursor(dictionary=True)
    try:
        mc.execute("SELECT * FROM customers;")
        r = mc.fetchall()
        return jsonify(r)
    finally:
        mc.close()
        mydb.close()

# 2. Display all accounts[cite: 4]
@app.route("/customers/accounts", methods=["GET"])
def accounts():
    mydb = config.connect()  #[cite: 2, 4]
    mc = mydb.cursor(dictionary=True)
    try:
        mc.execute('SELECT * FROM accounts')
        r = mc.fetchall()
        return jsonify(r)
    finally:
        mc.close()
        mydb.close()

# 3. Display customer transactions join view[cite: 4]
@app.route("/customers/transactions", methods=["GET"])
def transactions():
    mydb = config.connect()  #[cite: 2, 4]
    mc = mydb.cursor(dictionary=True)
    try:
        mc.execute('''
            SELECT  
                c.customer_id,
                c.name,
                a.account_type,
                t.transaction_type,
                t.amount 
            FROM customers as c 
            INNER JOIN accounts as a 
                ON c.customer_id = a.customer_id 
            INNER JOIN transactions as t 
                ON a.account_id = t.account_id;
        ''')
        r = mc.fetchall()
        return jsonify(r)
    finally:
        mc.close()
        mydb.close()

# Updated Add Customer Endpoint (Creates Customer + Unique Account)
@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json()
    if not data or "name" not in data or "account_type" not in data:
        return jsonify({"error": "Please provide a valid JSON body with 'name' and 'account_type'."}), 400

    db = config.connect()
    cur = db.cursor()
    try:
        # 1. Insert the new customer into the customers table
        cur.execute("INSERT INTO customers (name) VALUES (%s)", (data["name"],))
        customer_id = cur.lastrowid  # Retrieve the newly generated customer ID

        # 2. Create a unique account linked to this customer ID
        cur.execute(
            "INSERT INTO accounts (customer_id, account_type) VALUES (%s, %s)",
            (customer_id, data["account_type"])
        )
        db.commit()

        return jsonify({
            "message": "Added new customer and account successfully",
            "customer_id": customer_id,
            "account_type": data["account_type"]
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": "Failed to add customer and account", "details": str(e)}), 500
    finally:
        cur.close()
        db.close()
# ==========================================
# 5. NEW: ADD NEW TRANSACTION ENDPOINT (POST)
# ==========================================
@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Please provide transaction details in JSON format"}), 400

    required_fields = ["account_id", "transaction_date", "transaction_type", "amount", "description"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": "Missing required fields", "missing_fields": missing_fields}), 400

    db = config.connect()  #[cite: 2, 4]
    cur = db.cursor()
    try:
        query = """
            INSERT INTO transactions
            (account_id, transaction_date, transaction_type, amount, description_optional)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data["account_id"],
            data["transaction_date"],
            data["transaction_type"],
            data["amount"],
            data["description"]
        )
        cur.execute(query, values)
        db.commit()
        transaction_id = cur.lastrowid

        return jsonify({
            "message": "Transaction added successfully",
            "transaction_id": transaction_id,
            "data": data
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Failed to add transaction", "details": str(e)}), 500
    finally:
        cur.close()
        db.close()


# ==========================================
# REMOVE CUSTOMER & DATA BY ACCOUNT ID
# ==========================================
@app.route("/customers/delete-by-account", methods=["POST"])
def delete_customer_by_account():
    data = request.get_json()
    if not data or "account_id" not in data:
        return jsonify({"error": "Please provide a valid account_id."}), 400

    account_id = data["account_id"]
    db = config.connect()
    cur = db.cursor(dictionary=True)
    try:
        # 1. Find customer_id associated with this account_id
        cur.execute("SELECT customer_id FROM accounts WHERE account_id = %s", (account_id,))
        result = cur.fetchone()
        if not result:
            return jsonify({"error": "Account ID not found in database."}), 404

        customer_id = result["customer_id"]

        # 2. Get all account IDs belonging to this customer
        cur.execute("SELECT account_id FROM accounts WHERE customer_id = %s", (customer_id,))
        accounts_result = cur.fetchall()
        account_ids = [acc["account_id"] for acc in accounts_result]

        if account_ids:
            # Format accounts for SQL IN clause safely
            format_strings = ','.join(['%s'] * len(account_ids))

            # 3. Delete all transactions linked to these accounts
            cur.execute(f"DELETE FROM transactions WHERE account_id IN ({format_strings})", tuple(account_ids))

            # 4. Delete the accounts
            cur.execute("DELETE FROM accounts WHERE customer_id = %s", (customer_id,))

        # 5. Get customer name for message response
        cur.execute("SELECT name FROM customers WHERE customer_id = %s", (customer_id,))
        cust_res = cur.fetchone()
        customer_name = cust_res["name"] if cust_res else "Customer"

        # 6. Delete the customer record
        cur.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        db.commit()

        return jsonify({
            "message": f"Successfully removed customer '{customer_name}' and all associated accounts/transactions.",
            "customer_id": customer_id
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": "Failed to delete customer data", "details": str(e)}), 500
    finally:
        cur.close()
        db.close()

@app.route("/generate-chart", methods=["GET"])
def generate_chart():
    try:
        mydb = config.connect()  #[cite: 2, 4]
        df = pd.read_sql("SELECT * FROM transactions;", mydb)
        mydb.close()

        summary_df = df.groupby('transaction_type')['amount'].sum().reset_index()

        plt.figure(figsize=(8, 5))
        plt.bar(summary_df['transaction_type'], summary_df['amount'], color=['#2ecc71', '#e74c3c'])
        plt.title('Total Amount: Deposits vs Withdrawals', fontsize=14, fontweight='bold')
        plt.xlabel('Transaction Type', fontsize=12)
        plt.ylabel('Total Amount ($)', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        os.makedirs('static', exist_ok=True)
        chart_path = os.path.join('static', 'transaction_chart.png')
        plt.savefig(chart_path)
        plt.close()

        return jsonify({
            "message": "Chart generated successfully!",
            "image_url": "/static/transaction_chart.png"
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate chart", "details": str(e)}), 500



@app.route("/generate-customer-chart", methods=["GET"])
def generate_customer_chart():
    try:
        mydb = config.connect()  #[cite: 2, 4]
        query = """
            SELECT 
                c.name, 
                t.transaction_type, 
                t.amount 
            FROM customers AS c 
            INNER JOIN accounts AS a 
                ON c.customer_id = a.customer_id 
            INNER JOIN transactions AS t 
                ON a.account_id = t.account_id;
        """
        df = pd.read_sql(query, mydb)
        mydb.close()

        if df.empty:
            return jsonify({"error": "No transaction data found for customers."}), 404

        pivot_df = df.pivot_table(
            index='name',
            columns='transaction_type',
            values='amount',
            aggfunc='sum'
        ).fillna(0)

        fig, ax = plt.subplots(figsize=(10, 6))
        pivot_df.plot(kind='bar', ax=ax, color=['#2ecc71', '#e74c3c'], width=0.7)

        plt.title('Transaction Analysis: Deposits vs Withdrawals per Customer', fontsize=14, fontweight='bold')
        plt.xlabel('Customer Name', fontsize=12)
        plt.ylabel('Total Amount ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(['DEPOSIT', 'WITHDRAWAL'])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        os.makedirs('static', exist_ok=True)
        chart_path = os.path.join('static', 'customer_transaction_chart.png')
        plt.savefig(chart_path)
        plt.close()

        return jsonify({
            "message": "Customer transaction chart generated successfully!",
            "image_url": "/static/customer_transaction_chart.png"
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate customer chart", "details": str(e)}), 500



@app.route("/dashboard", methods=["GET"])
def dashboard():
    mydb = config.connect()  #[cite: 2, 4]
    mc = mydb.cursor(dictionary=True)
    try:
        mc.execute("""
            SELECT 
                t.transaction_id,
                c.name,
                a.account_type,
                t.transaction_date,
                t.transaction_type,
                t.amount,
                t.description_optional AS description
            FROM customers AS c
            INNER JOIN accounts AS a 
                ON c.customer_id = a.customer_id
            INNER JOIN transactions AS t 
                ON a.account_id = t.account_id
            ORDER BY t.transaction_id DESC
            LIMIT 10;
        """)
        recent_transactions = mc.fetchall()
        return render_template("index.html", transactions=recent_transactions)
    finally:
        mc.close()
        mydb.close()


if __name__ == "__main__":
    app.run(debug=True)
