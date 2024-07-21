from flask import Flask, jsonify
from peewee import Model, IntegerField, SqliteDatabase
import os

app = Flask(__name__)

# Configure the database
db = SqliteDatabase('views.db')

class BaseModel(Model):
    class Meta:
        database = db

class ViewCount(BaseModel):
    count = IntegerField(default=0)

# Create the tables if they don't exist
with app.app_context():
    db.connect()
    db.create_tables([ViewCount], safe=True)

@app.route('/increment')
def increment_views():
    view_count, created = ViewCount.get_or_create()
    view_count.count += 1
    view_count.save()
    return jsonify({"views": view_count.count})

@app.route('/count')
def get_count():
    view_count = ViewCount.select().first()
    return jsonify({"views": view_count.count if view_count else 0})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get PORT from environment or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)  # Use the retrieved port
