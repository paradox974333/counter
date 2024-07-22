from flask import Flask, jsonify
from peewee import Model, IntegerField, PostgresqlDatabase
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure database connection
db = PostgresqlDatabase(
    os.getenv('DB_NAME', 'postgres'),
    user=os.getenv('DB_USER', 'postgres.fmgtdwisxldecgkzdnuf'),
    password=os.getenv('DB_PASSWORD', 'UC0reusq9SlUzTq5'),
    host=os.getenv('DB_HOST', 'aws-0-ap-south-1.pooler.supabase.com'),
    port=os.getenv('DB_PORT', 6543)
)

# Define BaseModel for Peewee models
class BaseModel(Model):
    class Meta:
        database = db

# Define ViewCount model
class ViewCount(BaseModel):
    count = IntegerField(default=0)

# Function to initialize database tables
def initialize_database():
    try:
        with db:
            db.create_tables([ViewCount], safe=True)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

# Endpoint to increment views
@app.route('/increment', methods=['GET'])
def increment_views():
    try:
        with db.atomic():
            view_count, created = ViewCount.get_or_create(id=1)
            view_count.count += 1
            view_count.save()
        logger.info(f"Views incremented. New count: {view_count.count}")
        return jsonify({"views": view_count.count}), 200
    except Exception as e:
        logger.error(f"Error incrementing views: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint to get current count
@app.route('/count', methods=['GET'])
def get_count():
    try:
        view_count, created = ViewCount.get_or_create(id=1)
        logger.info(f"Count retrieved: {view_count.count}")
        return jsonify({"views": view_count.count}), 200
    except Exception as e:
        logger.error(f"Error retrieving count: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    try:
        initialize_database()
        port = int(os.getenv('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')
    except Exception as e:
        logger.critical(f"Failed to start the application: {e}")
