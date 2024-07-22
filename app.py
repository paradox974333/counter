from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# File to store the view count
COUNT_FILE = 'view_count.txt'

def get_count():
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            return int(f.read() or 0)
    return 0

def save_count(count):
    with open(COUNT_FILE, 'w') as f:
        f.write(str(count))

@app.route('/increment', methods=['GET'])
def increment_views():
    count = get_count() + 1
    save_count(count)
    return jsonify({"views": count}), 200

@app.route('/count', methods=['GET'])
def get_view_count():
    count = get_count()
    return jsonify({"views": count}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
