from flask import Flask, jsonify
from peewee import Model, IntegerField, SqliteDatabase
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Use a more permanent location for the database
db_path = os.path.join(os.path.dirname(__file__), 'persistent_views.db')
db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db

class ViewCount(BaseModel):
    count = IntegerField(default=0)

def initialize_database():
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