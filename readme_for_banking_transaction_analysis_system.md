# Banking Transaction Analysis System

## Overview
The Banking Transaction Analysis System is a comprehensive, full-stack local web application built using Python, Flask, MySQL, Pandas, and Matplotlib. Designed to streamline financial tracking and analytics, this platform bridges relational database management with dynamic data visualization. It allows users and administrators to seamlessly manage bank customers, track various account types (Savings and Current), record secure monetary transactions, and instantly translate raw database records into clear, actionable visual insights.

## Key Features
* **RESTful API Backend:** Powered by Flask to handle HTTP GET and POST requests for customers, accounts, and financial transactions.
* **Relational Database Integration:** Connects securely with a MySQL backend using `mysql-connector-python`, maintaining data integrity across customers, accounts, and transactions with proper foreign key constraints.
* **Data Science Analytics:** Leverages **Pandas** and **NumPy** to query, clean, aggregate, and pivot large volumes of transaction data directly from SQL tables.
* **Dynamic Chart Generation:** Employs **Matplotlib** in a headless server environment (`Agg`) to automatically generate and save high-resolution visual charts—such as overall deposit-versus-withdrawal comparisons and customer-specific grouped bar charts.
* **Interactive Web Dashboard:** Features Jinja2-powered HTML templating to present a clean, responsive analytics dashboard right in your local browser.

## Tech Stack
* **Backend:** Python, Flask, Werkzeug
* **Database:** MySQL, MySQL Connector
* **Data Analysis & Visualization:** Pandas, NumPy, Matplotlib
* **Frontend:** HTML5, CSS3, Jinja2 Templating

## Getting Started & Installation
1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install flask mysql-connector-python pandas matplotlib
   ```
3. Ensure your local MySQL server has the `bank_details` database configured.
4. Run the Flask application:
   ```bash
   python web.py
   ```
5. Open your browser and navigate to `http://127.0.0.1:5000/dashboard` to view the live analytics dashboard.