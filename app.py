from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage (resets when server restarts)
expenses = []

# Home - Show Expenses
@app.route('/')
def index():
    total = sum(expense['amount'] for expense in expenses)
    return render_template('index.html', expenses=expenses, total=total)

# Add Expense
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']
        date = request.form['date']

        new_expense = {
            'id': len(expenses) + 1,
            'amount': amount,
            'description': description,
            'date': date
        }
        expenses.append(new_expense)
        return redirect(url_for('index'))

    return render_template('add_expense.html')

# Delete Expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    global expenses
    expenses = [exp for exp in expenses if exp['id'] != id]
    return redirect(url_for('index'))

@app.route('/report')
def report():
    sorted_expenses = sorted(expenses, key=lambda x: x['date'], reverse=True)  # Sort by newest date
    total_spent = sum(exp['amount'] for exp in expenses)
    return render_template('report.html', total_spent=total_spent, expenses=sorted_expenses)


if __name__ == '__main__':
    app.run(debug=True)
