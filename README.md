# 💰 Personal Finance Tracker

A web-based personal finance tracker built with **Flask** and **SQLite**, allowing users to manage their financial transactions securely. Each user gets their own transaction table, and the system records deposits, withdrawals, balances, and descriptions of transactions.

---

## 🚀 Features

- 🔐 **User Authentication**: Secure login and registration for users.
- 📊 **Transaction Recording**: Log deposits and withdrawals with optional descriptions.
- 📂 **User-Specific Tables**: Each user has a dynamically created transaction table.
- 📅 **Timestamping**: Automatically records the date and time of each transaction.
- 🧾 **Transaction History**: Displays all past transactions and current balance.
- 🧠 **Smart Table Creation**: Dynamically creates tables only if they don’t exist, using SQLAlchemy's `inspect`.

---

## 🛠 Technologies & Techniques Used

| Area                  | Details                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| 🧱 Backend Framework   | [Flask](https://flask.palletsprojects.com/) - lightweight Python web framework |
| 🗄️ Database            | [SQLite](https://www.sqlite.org/) - embedded relational DB, ideal for lightweight apps |
| ⚙ ORM & DB Management | [SQLAlchemy](https://www.sqlalchemy.org/) - object-relational mapping for database operations |
| 📅 Time Management     | Python's `datetime` module to record transaction time                   |
| 🧪 Table Introspection | SQLAlchemy’s `inspect()` used to check if user tables already exist     |
| 🧰 Templates           | HTML pages rendered using Flask’s `render_template` function            |
| 🧩 Dynamic Routing     | Custom URL for each user (e.g., `/john_doe`)                            |

---

## ✅ Requirements to run the app

1. Create a Virtual Environment (Recommended)
2. Activate the Virtual Environment
3. Install Required Libraires
4. Run the app.py, the link will be open in the browser with the local host






