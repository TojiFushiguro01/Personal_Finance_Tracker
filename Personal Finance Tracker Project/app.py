from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import inspect

# Initialize the Flask application
app = Flask(__name__)

# Set up the database URI and configurations
app.config["SERVER_NAME"] = "localhost:5000"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./Finance.db'  # Using SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app


# Dynamically create the Account model for each user
def create_account(table_name):
    # Check if the table already exists in the database
    inspector = inspect(db.engine)
    if table_name in inspector.get_table_names():
        # If the table exists, don't redefine the model.
        class Account(db.Model):
            __tablename__ = table_name
            __table_args__ = {'extend_existing': True}  # Ensure existing table is extended
            sno = db.Column(db.Integer, primary_key=True)
            date = db.Column(db.DateTime, default=datetime.utcnow)
            desc = db.Column(db.String(500), nullable=True)
            opr = db.Column(db.String(10), nullable=False)
            amount = db.Column(db.Integer, nullable=False)
            balance = db.Column(db.Integer, nullable=False)
        return Account

    # If the table doesn't exist, define the model dynamically and create it.
    class Account(db.Model):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}  # Ensure existing table is extended
        sno = db.Column(db.Integer, primary_key=True)
        date = db.Column(db.DateTime, default=datetime.utcnow)
        desc = db.Column(db.String(500), nullable=True)
        opr = db.Column(db.String(10), nullable=False)
        amount = db.Column(db.Integer, nullable=False)
        balance = db.Column(db.Integer, nullable=False)

    # Create the table if it doesn't already exist
    db.create_all()
    return Account


# Define the 'User' model for storing user login credentials
class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)  # Primary key for user
    username = db.Column(db.String(100), unique=True, nullable=False)  # Unique username
    password = db.Column(db.String(100), nullable=False)  # Password for authentication


# Route to handle the login page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        AccountName = request.form.get('AccountName')
        Password = request.form.get('Password')

        user = User.query.filter_by(username=AccountName).first()
        if user and user.password == Password:
            return redirect(f'/{AccountName}')
        else:
            return redirect(f'/Register')  

    return render_template("home.html")


# Route to handle Registration
@app.route("/Register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        AccountName = request.form.get('AccountName')

        # Register User in the database
        new_user = User(username=AccountName, password=request.form.get('Password'))
        db.session.add(new_user)
        db.session.commit()

        # Dynamically create a transactions table for the user
        create_account(AccountName)

        return redirect(f'/{AccountName}')

    return render_template("register.html")


# Route to display the user's account page (authenticated users only)
@app.route('/<string:AccountName>', methods=['GET', 'POST'])
def show_account(AccountName):
    model = create_account(AccountName)

    if request.method == 'POST':
        desc = request.form.get('Description')
        withdraw_amount = request.form.get('Withdraw')
        deposit_amount = request.form.get('Deposit')

        last_transaction = model.query.order_by(model.sno.desc()).first()
        current_balance = last_transaction.balance if last_transaction else 0

        if withdraw_amount:
            withdraw_amount = int(withdraw_amount)
            if current_balance >= withdraw_amount:
                new_balance = current_balance - withdraw_amount
                new_withdraw = model(
                    opr="Withdraw",
                    desc=desc,
                    amount=withdraw_amount,
                    balance=new_balance
                )
                db.session.add(new_withdraw)
                db.session.commit()

        if deposit_amount:
            deposit_amount = int(deposit_amount)
            new_balance = current_balance + deposit_amount
            new_deposit = model(
                opr="Deposit",
                desc=desc,
                amount=deposit_amount,
                balance=new_balance
            )
            db.session.add(new_deposit)
            db.session.commit()

    transactions = model.query.all()
    return render_template("account.html", AccountName=AccountName, transactions=transactions)


# Route for the 'About' page
@app.route("/About")
def about():
    return render_template("about.html")


# Ensure that the database tables are created if they don't exist
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables (including User and any dynamic Account tables)

    app.run(debug=True)
