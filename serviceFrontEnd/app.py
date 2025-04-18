import uuid
import json
import logging
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.FileHandler("serviceFrontEnd.log"), logging.StreamHandler()])


r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing message in request'}), 400

    original_message = data['message']
    message_id = str(uuid.uuid4())
  
    processed_message = original_message + "_serviceFrontEnd"
    payload = {
        "id": message_id,
        "message": processed_message
    }
  
    logging.info(json.dumps({"event": "received", "service": "serviceFrontEnd", "id": message_id, "message": processed_message}))
    
    
    r.incr("total_sent")
    r.hset(f"message:{message_id}", mapping={"state": "processed by serviceFrontEnd"})
    
  
    r.rpush("queue:serviceA", json.dumps(payload))
    
    return jsonify({"status": "processing", "id": message_id}), 200

@app.route('/complete', methods=['POST'])
def complete():
    data = request.get_json()
    if not data or 'id' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    message_id = data['id']
    final_message = data['message']
    logging.info(json.dumps({"event": "completed", "service": "serviceFrontEnd", "id": message_id, "final_message": final_message}))
 
    r.hset(f"message:{message_id}", "state", "completed at serviceFrontEnd")
    return jsonify({"status": "complete", "id": message_id, "final_message": final_message}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
