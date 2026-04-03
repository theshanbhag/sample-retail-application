import os
import json
from pymongo import MongoClient
from bson import json_util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_data_to_mongodb():
    # Configuration
    connection_string = os.getenv("MDB_MCP_CONNECTION_STRING")
    if not connection_string:
        print("Error: MDB_MCP_CONNECTION_STRING not found in environment variables.")
        return

    file_path = "data/search_catalog_myn.json"
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        db = client.search
        collection = db.catalog_products

        # Read and parse JSON data with BSON support
        print(f"Reading data from {file_path}...")
        with open(file_path, 'r') as f:
            data = json_util.loads(f.read())
            
        if not isinstance(data, list):
            data = [data]

        print(f"Loading {len(data)} records into MongoDB...")
        
        # Clear existing data if needed (optional, but good for idempotency)
        # collection.delete_many({})
        
        result = collection.insert_many(data)
        print(f"Successfully loaded {len(result.inserted_ids)} records.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load_data_to_mongodb()
