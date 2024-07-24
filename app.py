from flask import Flask, jsonify
import os
import threading
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

VIEW_COUNT = 0
count_lock = threading.Lock()

def get_view_count():
    global VIEW_COUNT
    with count_lock:
        return VIEW_COUNT

def increment_view_count():
    global VIEW_COUNT
    with count_lock:
        VIEW_COUNT += 1
        return VIEW_COUNT

@app.route('/increment', methods=['GET'])
def increment_views():
    try:
        count = increment_view_count()
        logging.info(f"Incremented count to {count}")
        return jsonify({"views": count})
    except Exception as e:
        logging.error(f"Error in increment_views: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/count', methods=['GET'])
def get_count():
    try:
        count = get_view_count()
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
