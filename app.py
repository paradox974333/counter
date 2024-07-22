from flask import Flask, jsonify
import os

app = Flask(__name__)

VIEW_COUNT_FILE = 'view_count.txt'

def get_view_count():
    if not os.path.exists(VIEW_COUNT_FILE):
        with open(VIEW_COUNT_FILE, 'w') as f:
            f.write('0')
    with open(VIEW_COUNT_FILE, 'r') as f:
        try:
            return int(f.read().strip())
        except ValueError:
            # If the file contains invalid data, reset to 0
            return 0

def increment_view_count():
    count = get_view_count() + 1
    with open(VIEW_COUNT_FILE, 'w') as f:
        f.write(str(count))
    return count

@app.route('/increment', methods=['GET'])
def increment_views():
    count = increment_view_count()
    return jsonify({"views": count})

@app.route('/count', methods=['GET'])
def get_count():
    count = get_view_count()
    return jsonify({"views": count})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True)
