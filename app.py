from flask import Flask, jsonify
from peewee import Model, IntegerField, PostgresqlDatabase
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure database connection
db = PostgresqlDatabase(
    'postgres',  # Replace with your database name
    user='postgres.fmgtdwisxldecgkzdnuf',  # Replace with your database username
    password='UC0reusq9SlUzTq5',  # Replace with your database password
    host='aws-0-ap-south-1.pooler.supabase.com',  # Replace with your database host
    port=6543  # Replace with your database port
)

# Define BaseModel for Peewee models
class BaseModel(Model):
    class Meta:
        database = db

# Define your ViewCount model
class ViewCount(BaseModel):
    count = IntegerField(default=0)

# Function to initialize database tables
def initialize_database():
    with db:
        db.create_tables([ViewCount], safe=True)

# Endpoint to increment views
@app.route('/increment', methods=['GET'])
def increment_views():
    try:
        with db.atomic():
            view_count, created = ViewCount.get_or_create(id=1)
            view_count.count += 1
            view_count.save()
        return jsonify({"views": view_count.count}), 200
    except Exception as e:
        app.logger.error(f"Error incrementing views: {e}")
        return jsonify({"error": str(e)}), 500

# Endpoint to get current count
@app.route('/count', methods=['GET'])
def get_count():
    try:
        view_count, created = ViewCount.get_or_create(id=1)
        return jsonify({"views": view_count.count}), 200
    except Exception as e:
        app.logger.error(f"Error retrieving count: {e}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    initialize_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
