import os
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Environment variables for K8s flexibility
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo:27017/')
client = MongoClient(MONGO_URI)
db = client.microstore
products_col = db.products

# Initialize DB with some dummy data if empty
if products_col.count_documents({}) == 0:
    products_col.insert_many([
        {"id": "1", "name": "Laptop", "quantity": 10},
        {"id": "2", "name": "Mouse", "quantity": 50}
    ])

@app.route('/products', methods=['GET'])
def get_products():
    # Convert Mongo objects to JSON friendly format
    products = []
    for doc in products_col.find():
        products.append({
            "id": doc["id"],
            "name": doc["name"],
            "quantity": doc["quantity"]
        })
    return jsonify(products)

@app.route('/order', methods=['POST'])
def order_product():
    data = request.get_json()
    product_id = data.get('product_id')

    # Simple logic: Find product and decrease quantity
    result = products_col.update_one(
        {"id": product_id, "quantity": {"$gt": 0}},
        {"$inc": {"quantity": -1}}
    )

    if result.modified_count > 0:
        return jsonify({"status": "success", "message": "Stock updated"}), 200
    else:
        return jsonify({"status": "error", "message": "Out of stock or invalid ID"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)