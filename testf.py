import sqlite3
from bank_crud_sqlite import create_account, deposit, withdraw, get_balance

def test_create_account():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL)")
    conn.execute("CREATE TABLE transactions (id INTEGER PRIMARY KEY, account_id INTEGER, type TEXT, amount REAL, timestamp TEXT, description TEXT)")
    account_id = create_account("Test User", 500)
    assert account_id is not None

def test_deposit():
    account_id = create_account("Tester", 1000)
    deposit(account_id, 500)
    assert get_balance(account_id) == 1500

def test_withdraw():
    account_id = create_account("Withdraw Test", 1000)
    withdraw(account_id, 300)
    assert get_balance(account_id) == 700
