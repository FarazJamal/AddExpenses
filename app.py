from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField
from datetime import datetime, time

app = Flask(__name__)
app.config["SECRET_KEY"]="include_a_strong_secret_key"
app.config["MONGO_URI"] = "mongodb+srv://faraz:LJeHqecZe2E5xa9M@cluster0.9otkocy.mongodb.net/db.expenses?retryWrites=true&w=majority"

mongo = PyMongo(app)
mongo.init_app(app)

# create a class Expenses that extends FlaskForm
class Expenses(FlaskForm):
    # StringField for description
    description = StringField('Description')
    # SelectField for category
    category = SelectField('Category', choices=[('groceries', 'Groceries'), ('gas', 'Gas'), ('utilities', 'Utilities'), ('rent', 'Rent'), ('insurance', 'Insurance'), ('transportation', 'Transportation'), ('entertainment', 'Entertainment')])
    # DecimalField for cost
    cost = DecimalField('Cost')
    # DateField for date
    date = DateField('Date')

# define a function to get the total expenses of a specific category
def get_total_expenses(category):
    # find all the documents in the expenses collection that match the category
    my_expenses = mongo.db.expenses.find({'category': category})
    total_cost = 0
    # iterate through the documents and add up the cost field
    for i in my_expenses:
        total_cost += float(i["cost"])
    return total_cost

@app.route('/')
def index():
    # find all the documents in the expenses collection
    my_expenses = mongo.db.expenses.find()
    total_cost = 0
    # iterate through the documents and add up the cost field
    for i in my_expenses:
        total_cost += float(i["cost"])
    # create a list of tuples, where each tuple contains the category label and the total cost of that category
    expensesByCategory = [("groceries" , get_total_expenses("groceries")), ("utilities" , get_total_expenses("utilities")), ("rent" , get_total_expenses("rent")), ("insurance" , get_total_expenses("insurance")), ("transportation" , get_total_expenses("transportation")), ("entertainment" , get_total_expenses("entertainment"))]
    return render_template("index.html", expenses=total_cost, expensesByCategory=expensesByCategory)

@app.route('/addExpenses', methods=['GET', 'POST'])
def addExpenses():
    expensesForm = Expenses(request.form)
    if request.method == 'POST' and expensesForm.validate():
        new_expense = {
            'description': expensesForm.description.data,
            'cost': float(expensesForm.cost.data),  # Convert Decimal to float
            'category': expensesForm.category.data,
            'date': datetime.combine(expensesForm.date.data, time.min)
        }
        mongo.db.expenses.insert_one(new_expense)
        return redirect(url_for('index'))
    return render_template("addExpenses.html", form=expensesForm)

if __name__ == '__main__':
    app.run(debug=True)
