from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import os
from pymongo.errors import ConnectionFailure

app = Flask(__name__)
CORS(app)

# MongoDB configuration
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI", "mongodb+srv://manoj123l299:manoj@9945@bookstore.6lt9uuw.mongodb.net/?retryWrites=true&w=majority&appName=bookstore")
mongo = PyMongo(app)

@app.route('/increment', methods=['GET'])
def increment_views():
    try:
        result = mongo.db.views.find_one_and_update(
            {"_id": "view_counter"},
            {"$inc": {"count": 1}},
            upsert=True,
            return_document=True
        )
        count = result['count']
        return jsonify({"views": count}), 200
    except ConnectionFailure:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/count', methods=['GET'])
def get_view_count():
    try:
        result = mongo.db.views.find_one({"_id": "view_counter"})
        count = result['count'] if result else 0
        return jsonify({"views": count}), 200
    except ConnectionFailure:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Ping the database to check connection
        mongo.db.command('ping')
        return jsonify({"status": "healthy"}), 200
    except ConnectionFailure:
        return jsonify({"status": "unhealthy", "error": "Database connection failed"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
