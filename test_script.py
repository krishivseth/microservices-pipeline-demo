import time
import requests
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def send_single_message():
    url = "http://localhost:5001/process"  # Adjust if needed
    payload = {"message": "TestMessage"}
    response = requests.post(url, json=payload)
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    try:
        data = response.json()
        print("Single message response:", data)
    except Exception as e:
        print("Error decoding JSON:", e)

def send_batch_messages(n=100):
    url = "http://localhost:5001/process"
    for i in range(n):
        payload = {"message": f"BatchMessage_{i}"}
        try:
            response = requests.post(url, json=payload, timeout=5)
            print(f"Sent message {i}: {response.json()}")
        except Exception as e:
            print(f"Error sending message {i}: {e}")

def print_statistics():
    total_sent = int(r.get("total_sent") or 0)
    success = int(r.get("success_count") or 0)
    failed = int(r.get("failed_count") or 0)
    stuck = total_sent - (success + failed)
    print("\nMessage Processing Statistics:")
    print("Total messages sent:", total_sent)
    print("Successful messages:", success)
    print("Failed messages:", failed)
    print("Stuck messages:", stuck)

if __name__ == "__main__":
    print("Sending single message...")
    send_single_message()
    time.sleep(2)
    print("\nSending single message again...")
    send_single_message()
    time.sleep(2)
    print("\nSending batch messages...")
    send_batch_messages(100)
    time.sleep(10)
    print_statistics()
