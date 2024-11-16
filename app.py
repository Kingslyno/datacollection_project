from flask import Flask, render_template, url_for, request, redirect
from flask_cors import CORS
from pymongo import MongoClient
import csv
import pandas as pd

app = Flask(__name__)
CORS(app)

app = Flask(__name__, template_folder='views')

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['user_data']
collection = db['users']


class User:
    def __init__(self, name, age, gender, total_income, expenses):
        self.name = name
        self.age = age
        self.gender = gender
        self.total_income = total_income
        self.expenses = expenses

    def save_to_csv(self):
        with open('user_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.name, self.age, self.gender, self.total_income, self.expenses])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    total_income = request.form['total_income']

    expenses = {

       'utilities': request.form.get('utliities',0),
       'entertainment': request.form.get('entertainment',0),
       'school_fees': request.form.get('school_fees', 0),
       'shopping': request.form.get('shopping', 0),
       'healthcare': request.form.get('healthcare', 0)
    }

    # Store data in MongoDB
    user_data = {
        'name': name,
        'age': age,
        'gender': gender,
        'total_income': total_income,
        'expenses': expenses
    }
    collection.insert_one(user_data)

    # Create User instance and save to CSV
    user = User(name, age, gender, total_income, expenses)
    collection.insert_one(user.__dict__)
    user.save_to_csv()

    return redirect('/successful')

if __name__ == '__main__':
    app.run(debug=True)