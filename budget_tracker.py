from flask import Flask, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)

# Initialize the CSV file (if not already exists)
def initialize_file():
    try:
        with open("expenses.csv", mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount"])
    except FileExistsError:
        pass

# Add expense route
@app.route('/', methods=['GET', 'POST'])
def view_expenses():
    if request.method == 'POST':
        # Handle form submission for adding an expense
        category = request.form['category']
        amount = request.form['amount']
        date = datetime.now().strftime("%Y-%m-%d")
        try:
            with open("expenses.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, category, float(amount)])
            return redirect(url_for('view_expenses'))
        except ValueError:
            return "Invalid amount. Please enter a numeric value."
    
    try:
        with open("expenses.csv", mode='r') as file:
            reader = csv.reader(file)
            expenses = list(reader)

        # Display the form to add expense and expenses as a table
        result = '''
            <h2>Add Expense</h2>
            <form method="POST">
                Category: <input type="text" name="category"><br>
                Amount: <input type="text" name="amount"><br>
                <input type="submit" value="Add Expense">
            </form><br>

            <h2>Expenses</h2>
            <table border='1'>
                <tr><th>Date</th><th>Category</th><th>Amount</th></tr>'''
        
        for row in expenses[1:]:  # Skip header row
            result += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
        
        result += "</table>"
        return result
    except FileNotFoundError:
        return "No expenses found. Please add an expense first."

# Summary route
@app.route('/summary')
def generate_summary():
    try:
        category_totals = {}
        with open("expenses.csv", mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                category = row[1]
                amount = float(row[2])
                category_totals[category] = category_totals.get(category, 0) + amount
        
        # Display summary report
        result = "<h2>Summary Report</h2><ul>"
        for category, total in category_totals.items():
            result += f"<li>{category}: ₹{total}</li>"
        result += "</ul>"
        return result
    except FileNotFoundError:
        return "No expenses found. Please add an expense first."

# Run the app
if __name__ == '__main__':
    initialize_file()  # Ensure the file is initialized
    app.run(debug=True)
