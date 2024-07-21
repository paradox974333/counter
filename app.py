from flask import Flask, jsonify
from peewee import Model, IntegerField, SqliteDatabase
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict
import os

app = Flask(__name__)
CORS(app)

db = SqliteDatabase('views.db')

class BaseModel(Model):
    class Meta:
        database = db

class ViewCount(BaseModel):
    count = IntegerField(default=0)

with app.app_context():
    db.connect()
    db.create_tables([ViewCount], safe=True)

@app.route('/increment')
def increment_views():
    try:
        with db.atomic():
            view_count, created = ViewCount.get_or_create(id=1)
            ViewCount.update(count=ViewCount.count + 1).where(ViewCount.id == 1).execute()
            updated_count = ViewCount.get(ViewCount.id == 1).count
        return jsonify({"views": updated_count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/count')
def get_count():
    try:
        view_count = ViewCount.get_or_create(id=1)[0]
        return jsonify({"views": view_count.count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
