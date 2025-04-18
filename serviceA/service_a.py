import json
import logging
import redis


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.FileHandler("serviceA.log"), logging.StreamHandler()])


r = redis.Redis(host='redis', port=6379, decode_responses=True)

logging.info("serviceA waiting for messages on queue 'queue:serviceA'")

def process_message(message_data):
    try:
        data = json.loads(message_data)
        message_id = data["id"]
        msg = data["message"]
   
        new_msg = msg + "_serviceA"
        new_payload = {"id": message_id, "message": new_msg}
    
        logging.info(json.dumps({"event": "processed", "service": "serviceA", "id": message_id, "message": new_msg}))
    
        r.hset(f"message:{message_id}", "state", "processed by serviceA")

        r.rpush("queue:serviceB", json.dumps(new_payload))
    except Exception as e:
        logging.error(f"Error processing message in serviceA: {e}")

while True:
    try:
        _, message_data = r.blpop("queue:serviceA", timeout=0)
        process_message(message_data)
    except Exception as e:
        logging.error(f"Error in serviceA main loop: {e}")
