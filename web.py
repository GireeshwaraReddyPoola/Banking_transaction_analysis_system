import os
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, jsonify, request, render_template
import config

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "HELLO CUSTOMERS - BANKING TRANSACTION ANALYSIS SYSTEM"



@app.route("/customers", methods=["GET"])
def customers():
    mydb = config.connect()  # Calls connect() from config.py[cite: 2, 4]
    mc = mydb.cursor(dictionary=True)
    try:
        mc.execute("SELECT * FROM customers;")
        r = mc.fetchall()
        return jsonify(r)
    finally:
        mc.close()
        mydb.close()


# Display all accounts[cite: 4]
@app.route("/customers/accounts", methods=["GET"])
def accounts():
    mydb = config.connect()  # [cite: 2, 4]
    mc = mydb.cursor(dictionary=True)
    try:
        mc.execute('''SELECT * FROM accounts''')
        r = mc.fetchall()
        return jsonify(r)
    finally:
        mc.close()
        mydb.close()


# Display customer transactions[cite: 4]
@app.route("/customers/transactions", methods=["GET"])
def transactions():
    mydb = config.connect()  # [cite: 2, 4]
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



@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Please provide a valid JSON body with a 'name' field."}), 400

    db = config.connect()  # [cite: 2, 4]
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO customers (name) VALUES (%s)", (data["name"],))
        db.commit()
        return jsonify({"message": "added new customer"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Failed to add customer", "details": str(e)}), 500
    finally:
        cur.close()
        db.close()

@app.route("/dashboard", methods=["GET"])
def dashboard():

    return render_template("index.html")

@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Please provide transaction details in JSON format"}), 400

    required_fields = ["account_id", "transaction_date", "transaction_type", "amount", "description"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": "Missing required fields", "missing_fields": missing_fields}), 400

    db = config.connect()  # [cite: 2, 4]
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



@app.route("/generatechart", methods=["GET"])
def generate_chart():
    try:

        mydb = config.connect()
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
        chart_filename = 'transaction_chart.png'
        chart_path = os.path.join('static', chart_filename)

        plt.savefig(chart_path)
        plt.close()

        return jsonify({
            "message": "Chart generated successfully!",
            "image_url": f"/static/{chart_filename}"
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to generate chart", "details": str(e)}), 500



@app.route("/generatecustomerchart", methods=["GET"])
def generate_customer_chart():
    try:

        mydb = config.connect()


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

        # Plot deposits and withdrawals side-by-side per customer
        pivot_df.plot(kind='bar', ax=ax, color=['#2ecc71', '#e74c3c'], width=0.7)

        plt.title('Transaction Analysis: Deposits vs Withdrawals per Customer', fontsize=14, fontweight='bold')
        plt.xlabel('Customer Name', fontsize=12)
        plt.ylabel('Total Amount ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(['DEPOSIT', 'WITHDRAWAL'])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Ensure static directory exists and save the chart image
        os.makedirs('static', exist_ok=True)
        chart_path = os.path.join('static', 'customer_transaction_chart.png')
        plt.savefig(chart_path)
        plt.close()  # Free up memory

        return jsonify({
            "message": "Customer transaction chart generated successfully!",
            "image_url": "/static/customer_transaction_chart.png"
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to generate customer chart", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)