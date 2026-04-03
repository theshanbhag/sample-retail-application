import os
import flask
import json
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB setup
def get_db_collection():
    connection_string = os.getenv("MDB_MCP_CONNECTION_STRING")
    if not connection_string:
        return None
    try:
        client = MongoClient(connection_string)
        return client.search.catalog_products
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

inventory_collection = get_db_collection()

@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "message": "Catalog API is running"})

@app.route('/load-data')
def load_data():
    if inventory_collection is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    file_path = "data/search_catalog_myn.json"
    try:
        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found: {file_path}"}), 404
            
        with open(file_path, 'r') as f:
            data = json_util.loads(f.read())
            
        if not isinstance(data, list):
            # If it's a single object, wrap it in a list
            data = [data]
            
        result = inventory_collection.insert_many(data)
        return jsonify({
            "status": "success", 
            "message": f"Successfully loaded {len(result.inserted_ids)} records",
            "count": len(result.inserted_ids)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/categories')
def get_categories():
    if inventory_collection is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        categories = sorted(inventory_collection.distinct("masterCategory"))
        return jsonify(categories)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/inventory')
def get_inventory():
    if inventory_collection is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    category = request.args.get('category')
    
    try:
        query = {}
        if category and category != "All":
            query["masterCategory"] = category

        # Only return fields needed for list view
        projection = {
            "title": 1, 
            "link": 1, 
            "price": 1, 
            "masterCategory": 1,
            "_id": 1
        }
        
        cursor = inventory_collection.find(query, projection).limit(100)
        items = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            items.append(doc)
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/product/<product_id>')
def get_product(product_id):
    if inventory_collection is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        # Get full document for the specific product
        doc = inventory_collection.find_one({"_id": ObjectId(product_id)})
        if doc:
            doc['_id'] = str(doc['_id'])
            # Remove embedding if it exists for the detail view to keep it clean
            if 'embedding' in doc:
                del doc['embedding']
            return jsonify(doc)
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
