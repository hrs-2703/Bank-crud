import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect("bank.db")

def initialize_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                description TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
        """)
        conn.commit()

def create_account(name, initial_balance):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, initial_balance))
        account_id = cursor.lastrowid
        log_transaction(account_id, "deposit", initial_balance, "Account created with initial balance")
        return account_id

def update_balance(account_id, amount, transaction_type, description=""):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        conn.commit()
        log_transaction(account_id, transaction_type, amount, description)

def deposit(account_id, amount):
    update_balance(account_id, amount, "deposit", "Deposit made")

def withdraw(account_id, amount):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        balance = cursor.fetchone()
        if balance and balance[0] >= amount:
            update_balance(account_id, -amount, "withdrawal", "Withdrawal made")
        else:
            print("Insufficient funds.")

def log_transaction(account_id, transaction_type, amount, description):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (account_id, type, amount, timestamp, description)
            VALUES (?, ?, ?, ?, ?)
        """, (account_id, transaction_type, amount, datetime.now(), description))
        conn.commit()

def get_balance(account_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        balance = cursor.fetchone()
        return balance[0] if balance else None

def view_transactions(account_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE account_id = ?", (account_id,))
        return cursor.fetchall()

def main():
    initialize_db()
    account_id = create_account("Surya", 3000)
    print(f"New account created. ID: {account_id}")
    deposit(account_id, 500)
    withdraw(account_id, 200)
    print(f"Current balance: {get_balance(account_id)}")
    print("Transaction history:")
    for txn in view_transactions(account_id):
        print(txn)

if __name__ == "__main__":
    main()
