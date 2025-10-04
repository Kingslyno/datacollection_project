import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from flask import Flask, request, jsonify, render_template
import joblib
import os

# Step 1: Load dataset
file_path = r"C:\Users\kings\OneDrive\Desktop\NXU\Class\BAN6800\New folder\Module 3\Cleaned_dataset.csv"
df = pd.read_csv(file_path)

# Step 2: Explore dataset to identify relevant columns
# Assuming columns: 'books_available', 'books_sold', 'customer_id', 'books_purchased'
# If columns differ, adjust accordingly

# Step 3: Calculate quantities of books available and sold (summaries)
total_books_available = df['Quantity_Available'].sum()
total_books_sold = df['Quantity_Sold'].sum()

# Step 4: Customer ranking based on books purchased
customer_ranking = df.groupby('Customer_ID')['Amount_Paid'].sum().sort_values(ascending=False).reset_index()
customer_ranking['rank'] = customer_ranking['Amount_Paid'].rank(method='dense', ascending=False).astype(int)

# Step 5: Prepare data for linear regression model
# Predict books_sold based on books_available and possibly other features if available
# For simplicity, use books_available to predict books_sold

X = df[['Quantity_Available']]
y = df['Quantity_Sold']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Train linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 7: Evaluate model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Step 8: Visualize results
plt.figure(figsize=(10,6))
sns.scatterplot(x='Quantity_Available', y='Quantity_Sold', data=df, label='Actual')
plt.plot(X_test, y_pred, color='red', label='Predicted')
plt.title('Books Sold vs Books Available')
plt.xlabel('Books Available')
plt.ylabel('Books Sold')
plt.legend()
plt.tight_layout()
plt.savefig('books_sold_vs_available.png')
plt.close()

# Step 9: Save model for deployment
model_filename = 'linear_regression_books_model.pkl'
joblib.dump(model, model_filename)