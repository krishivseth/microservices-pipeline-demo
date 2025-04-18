#!/usr/bin/env python3
import time
import requests
import redis
import os
import argparse

def get_service_url():
    # Try to get service IP and port from environment or use defaults
    # For minikube, you may need to use `minikube service -n hsrn-vip servicefrontend --url`
    # For cloud providers, you might use an Ingress URL
    parser = argparse.ArgumentParser(description='Test the messaging pipeline')
    parser.add_argument('--host', default='localhost', help='The host of serviceFrontEnd')
    parser.add_argument('--port', default='80', help='The port of serviceFrontEnd')
    parser.add_argument('--redis-host', default='localhost', help='The Redis host')
    parser.add_argument('--redis-port', default='6379', help='The Redis port')
    parser.add_argument('--batch-size', type=int, default=100, help='Number of messages to send in batch')
    
    args = parser.parse_args()
    
    return args

def send_single_message(url):
    payload = {"message": "TestMessage"}
    response = requests.post(url, json=payload)
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    try:
        data = response.json()
        print("Single message response:", data)
    except Exception as e:
        print("Error decoding JSON:", e)

def send_batch_messages(url, n=100):
    for i in range(n):
        payload = {"message": f"BatchMessage_{i}"}
        try:
            response = requests.post(url, json=payload, timeout=5)
            print(f"Sent message {i}: {response.json()}")
        except Exception as e:
            print(f"Error sending message {i}: {e}")

def print_statistics(r):
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
    args = get_service_url()
    service_url = f"http://{args.host}:{args.port}/process"
    print(f"Using service URL: {service_url}")
    
    # Connect to Redis
    r = redis.Redis(host=args.redis_host, port=int(args.redis_port), decode_responses=True)
    
    print("Sending single message...")
    send_single_message(service_url)
    time.sleep(2)
    print("\nSending single message again...")
    send_single_message(service_url)
    time.sleep(2)
    print("\nSending batch messages...")
    send_batch_messages(service_url, args.batch_size)
    
    print("\nWaiting for messages to be processed...")
    for i in range(10):
        time.sleep(1)
        print(f"Checking statistics... ({i+1}/10)")
        print_statistics(r)
    
    print("\nFinal statistics:")
    print_statistics(r) 