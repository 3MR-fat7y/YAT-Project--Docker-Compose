from flask import Flask, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# Database connection function
def get_db_connection():
    client = MongoClient(os.getenv('MONGO_URI'))
    return client

@app.route('/')
def index():
    client = get_db_connection()
    db = client.get_default_database()
    collection = db['hits']
    
    hit = collection.find_one_and_update(
        {"page": "index"},
        {"$inc": {"count": 1}},
        upsert=True,
        return_document=True
    )
    
    count = hit["count"]
    return f"Hello, World! This page has been visited {count} times."

@app.route('/data')
def data():
    client = get_db_connection()
    db = client.get_default_database()
    collection = db['test']
    collection.insert_one({'message': 'Hello, Yat!'})
    message = collection.find_one({}, {'_id': 0})
    return jsonify(message)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
