import os
import requests
from flask import Flask, jsonify, render_template, redirect, url_for

app = Flask(__name__)

INVENTORY_SERVICE_URL = os.environ.get('INVENTORY_URL', 'http://inventory-service:5000')

@app.route('/')
def home():
    try:
        # 1. Call the Inventory Service to get the list of products
        response = requests.get(f"{INVENTORY_SERVICE_URL}/products")
        products = response.json()
    except Exception as e:
        # Fallback if inventory service is down
        products = []
        print(f"Error fetching inventory: {e}")

    # 2. Render the HTML template with the product data
    return render_template('index.html', products=products)

@app.route('/buy/<product_id>')
def buy_product(product_id):
    try:
        # Call the inventory to reduce stock
        response = requests.post(f"{INVENTORY_SERVICE_URL}/order", json={"product_id": product_id})

        # If successful, redirect back to home so the user sees the updated stock immediately
        if response.status_code == 200:
            return redirect(url_for('home'))
        else:
            return f"Error: {response.json().get('message')}", 400
    except Exception as e:
        return f"System Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)