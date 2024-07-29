from flask import Flask, jsonify
from flask_cors import CORS
import threading
import logging

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)

VIEW_COUNT = 0
count_lock = threading.Lock()

def increment_view_count():
    global VIEW_COUNT
    with count_lock:
        VIEW_COUNT += 1
        logging.info(f"Incremented count to {VIEW_COUNT}")
        return VIEW_COUNT

@app.route('/increment', methods=['GET'])
def increment_views():
    try:
        count = increment_view_count()
        return jsonify({"views": count})
    except Exception as e:
        logging.error(f"Error in increment_views: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/count', methods=['GET'])
def get_count():
    try:
        with count_lock:
            count = VIEW_COUNT
        logging.info(f"Retrieved count: {count}")
        return jsonify({"views": count})
    except Exception as e:
        logging.error(f"Error in get_count: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    logging.info("Health check called")
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
