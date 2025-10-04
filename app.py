# Step 10: Create Flask app for hosting model with simple front end
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from flask import Flask, request, jsonify, render_template

# Sample training data (replace with your actual data)
X = np.array([[10], [20], [30], [40], [50]])
y = np.array([8, 18, 28, 38, 48])

# Train the model
model = LinearRegression()
model.fit(X, y)

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Books Sold Prediction</h1>
    <form action="/predict" method="post">
      <label for="books_available">Books Available:</label><br>
      <input type="number" id="books_available" name="books_available" step="1" min="0" required><br><br>
      <input type="submit" value="Predict Books Sold">
    </form>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    try:
        books_available = float(request.form['books_available'])
        prediction = model.predict(np.array([[books_available]]))[0]
        prediction = max(0, round(prediction))  # Ensure no negative prediction
        return f'''
        <h1>Prediction Result</h1>
        <p>Books Available: {books_available}</p>
        <p>Predicted Books Sold: {prediction}</p>
        <a href="/">Back</a>
        '''
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # Run Flask app on localhost port 5000
    app.run(debug=True)
