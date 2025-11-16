from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)


# Initialize the database and create table if not exists
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        category TEXT,
                        amount REAL,
                        description TEXT
                    )''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch all expenses
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    # Total sum of all expenses
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    # ---------- Extra Features: Summary ----------

    # Get current month and year
    now = datetime.datetime.now()
    current_month = now.strftime("%Y-%m")
    
    # Total This Month
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ?", (current_month,))
    total_this_month = cursor.fetchone()[0]

    # Biggest Expense
    cursor.execute("SELECT MAX(amount) FROM expenses")
    biggest_expense = cursor.fetchone()[0]

    # Food Expenses
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE LOWER(category) = 'food'")
    food_expenses = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total if total else 0,
        total_this_month=total_this_month if total_this_month else 0,
        biggest_expense=biggest_expense if biggest_expense else 0,
        food_expenses=food_expenses if food_expenses else 0
    )


@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Get form data safely
        date = request.form.get('date')
        category = request.form.get('category')
        amount = request.form.get('amount')
        description = request.form.get('description')

        # Convert amount to float
        try:
            amount = float(amount)
        except:
            amount = 0.0

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insert into database
        cursor.execute("""
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        """, (date, category, amount, description))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("add_expense.html")


@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
