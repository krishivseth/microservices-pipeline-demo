# Microservices Demo for Artis Energy Internship Interview by Krishiv Seth

This project demonstrates a production-like environment built with Docker Compose and Python microservices. It showcases container orchestration, inter-service communication via middleware, structured logging, error handling, and testing.

## Overview

The following are the environment's components:

- **serviceFrontEnd**:  
  A Flask application that exposes a `/process` endpoint. It appends `_serviceFrontEnd` to an incoming message and forwards it to Service A.

- **serviceA**:  
  A Python microservice that listens for messages, appends `_serviceA` to the message, and forwards it to Service B.

- **serviceB**:  
  A Python microservice that randomly decides whether to:
  - Append `_serviceB_SUCCESS` to the message and forward it to Service Complete, or
  - Append `_FAILED` to the message and forward it to Service Complete.

- **serviceComplete**:  
  A Python microservice that logs the final message and sends a callback to the `/complete` endpoint of servicefrontend. It also updates counters in Redis for successful and failed messages.

- **Redis Middleware**:  
  Redis is used to decouple the microservices and facilitate asynchronous communication using Lists (RPUSH/BLPOP) to implement a reliable work queue pattern.

## Project Structure
   Each service has its own directory containing a Dockerfile and its corresponding Python code.

   ```
   ├── docker-compose.yml
   ├── README.md
   ├── test_script.py
   ├── serviceFrontEnd
   │   ├── Dockerfile
   │   └── app.py
   ├── serviceA
   │   ├── Dockerfile
   │   └── service_a.py
   ├── serviceB
   │   ├── Dockerfile
   │   └── service_b.py
   └── serviceComplete
       ├── Dockerfile
       └── service_complete.py
   ```

## Local Setup (Docker Compose)

### Prerequisites

- **Docker & Docker Compose**:  
  - **macOS & Windows**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and ensure it's running.
  - **Linux**: Install Docker and Docker Compose using your package manager or by following the [official installation guides](https://docs.docker.com/engine/install/).

- **Python 3.11** (for test script):  
  - Install Python 3.11 and create a virtual environment:
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install flask redis requests
    ```

### Building and Running Containers

1. **Build and start containers** in detached mode:
   ```bash
   docker compose up --build -d
   ```

2. **Verify the containers are running**:
   ```bash
   docker compose ps
   ```

3. **Run the test script**:
   ```bash
   python3.11 test_script.py
   ```

   Expected output will show:
   - Messages being processed
   - Final statistics of total, successful, and failed messages

## Kubernetes Deployment

This project can also be deployed to Kubernetes for a production-like environment:

1. **Deploy to Kubernetes**:
   ```bash
   ./deploy-to-k8s.sh
   ```

2. **Test the Kubernetes deployment**:
   ```bash
   ./k8s-test-script.py --host=<service-host> --port=<service-port>
   ```

For detailed Kubernetes deployment instructions, including scaling and monitoring, see the [Kubernetes README](k8s/README.md).

## Documentation

- **Architecture Report**: For a detailed explanation of the system architecture, technical decisions, and key learnings, see [architecture-report.md](architecture-report.md).

- **Kubernetes Guide**: For Kubernetes-specific deployment and operations, see [k8s/README.md](k8s/README.md).

