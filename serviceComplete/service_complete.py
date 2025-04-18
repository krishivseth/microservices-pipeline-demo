import json
import logging
import redis
import requests


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.FileHandler("serviceComplete.log"), logging.StreamHandler()])


r = redis.Redis(host='redis', port=6379, decode_responses=True)

logging.info("serviceComplete waiting for messages on queue 'queue:serviceComplete'")

def process_message(message_data):
    try:
        data = json.loads(message_data)
        message_id = data["id"]
        final_msg = data["message"]

        logging.info(json.dumps({"event": "final", "service": "serviceComplete", "id": message_id, "final_message": final_msg}))
   
        r.hset(f"message:{message_id}", "state", "processed by serviceComplete")
        
  
        if r.hsetnx(f"message:{message_id}", "counted", "1"):
            if final_msg.endswith("_serviceB_SUCCESS"):
                r.incr("success_count")
            elif "_FAILED" in final_msg:
                r.incr("failed_count")
        
        
        complete_url = "http://serviceFrontEnd:5000/complete"
        payload = {"id": message_id, "message": final_msg}
        try:
            response = requests.post(complete_url, json=payload, timeout=5)
            logging.info(json.dumps({"event": "callback", "service": "serviceComplete", "id": message_id, "status_code": response.status_code}))
        except Exception as e:
            logging.error(f"Error calling serviceFrontEnd /complete: {e}")
    except Exception as e:
        logging.error(f"Error processing message in serviceComplete: {e}")

while True:
    try:
        _, message_data = r.blpop("queue:serviceComplete", timeout=0)
        process_message(message_data)
    except Exception as e:
        logging.error(f"Error in serviceComplete main loop: {e}")
