from flask import Flask, jsonify, request
from peewee import Model, IntegerField, DateTimeField, SqliteDatabase
from flask_cors import CORS
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the database
db = SqliteDatabase('views.db')

class BaseModel(Model):
    class Meta:
        database = db

class ViewCount(BaseModel):
    count = IntegerField(default=0)
    date = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

# Create the tables if they don't exist
with app.app_context():
    db.connect()
    db.create_tables([ViewCount], safe=True)

@app.route('/increment', methods=['POST'])
def increment_views():
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    yesterday_start = today_start - timedelta(days=1)

    # Update today's count
    view_count_today, created = ViewCount.get_or_create(date=today_start)
    view_count_today.count += 1
    view_count_today.save()

    # Reset yesterday's count
    view_count_yesterday = ViewCount.select().where(ViewCount.date == yesterday_start).first()
    if view_count_yesterday:
        view_count_yesterday.count = 0
        view_count_yesterday.save()

    return jsonify({"message": "View count incremented", "views": view_count_today.count})

@app.route('/count')
def get_count():
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    yesterday_start = today_start - timedelta(days=1)

    # Retrieve counts
    view_count_today = ViewCount.select().where(ViewCount.date == today_start).first()
    view_count_yesterday = ViewCount.select().where(ViewCount.date == yesterday_start).first()

    return jsonify({
        "today": view_count_today.count if view_count_today else 0,
        "yesterday": view_count_yesterday.count if view_count_yesterday else 0
    })

@app.route('/online')
def get_online_count():
    # Placeholder for current online users
    return jsonify({"online_count": 0})  # Placeholder value

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)
