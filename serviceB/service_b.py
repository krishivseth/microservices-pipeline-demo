import json
import logging
import redis
import random


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.FileHandler("serviceB.log"), logging.StreamHandler()])


r = redis.Redis(host='redis', port=6379, decode_responses=True)

logging.info("serviceB waiting for messages on queue 'queue:serviceB'")

def process_message(message_data):
    try:
        data = json.loads(message_data)
        message_id = data["id"]
        msg = data["message"]
  
        if random.random() > 0.5:
            new_msg = msg + "_serviceB_SUCCESS"
        else:
            new_msg = msg + "_FAILED"
        new_payload = {"id": message_id, "message": new_msg}

        logging.info(json.dumps({"event": "processed", "service": "serviceB", "id": message_id, "message": new_msg}))

        r.hset(f"message:{message_id}", "state", "processed by serviceB")
   
        r.rpush("queue:serviceComplete", json.dumps(new_payload))
    except Exception as e:
        logging.error(f"Error processing message in serviceB: {e}")

while True:
    try:
        _, message_data = r.blpop("queue:serviceB", timeout=0)
        process_message(message_data)
    except Exception as e:
        logging.error(f"Error in serviceB main loop: {e}")
