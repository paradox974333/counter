from flask import Flask, jsonify
from peewee import Model, IntegerField, PostgresqlDatabase
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Use the connection string for database configuration
db = PostgresqlDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class ViewCount(BaseModel):
    count = IntegerField(default=0)

def initialize_database():
    db.init(os.environ['postgresql://postgres.fmgtdwisxldecgkzdnuf: UC0reusq9SlUzTq5@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'])
    with db:
        db.create_tables([ViewCount], safe=True)

@app.route('/increment')
def increment_views():
    try:
        with db.atomic():
            view_count, created = ViewCount.get_or_create(id=1)
            view_count.count += 1
            view_count.save()
        return jsonify({"views": view_count.count})
    except Exception as e:
        app.logger.error(f"Error incrementing views: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/count')
def get_count():
    try:
        view_count, created = ViewCount.get_or_create(id=1)
        return jsonify({"views": view_count.count})
    except Exception as e:
        app.logger.error(f"Error retrieving count: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    initialize_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)