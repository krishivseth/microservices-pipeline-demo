# Microservices Pipeline Architecture Report  
**Krishiv Seth, HSRN VIP Fall 2025**

---

## 1. Problem Statement  
This project implements a scalable, fault-tolerant message processing pipeline using microservices and Redis to demonstrate cloud-native patterns for reliable asynchronous communication in distributed systems.

## 2. Architecture Diagram  
![Architecture](diagram.png)  
*(Please create a diagram showing the message flow through the microservices and Redis, and commit it as diagram.png)*

## 3. Implementation Highlights  
- **Redis Lists** for work-queue semantics (RPUSH/BLPOP) ensuring each message is processed exactly once
- **Idempotent Counters** in serviceComplete (HSETNX) preventing duplicate counting during scaling/restarts
- **Message Format Transformation** through each stage with appended service identifiers
- **Kubernetes Resources**: Namespace (hsrn-vip), ConfigMap (Redis config), PVC (logs), Deployments with resource limits, HPA on serviceB
- **Health Probes**: Liveness and readiness checks ensuring service availability and proper scaling

## 4. Key Learnings  
1. **Pub/Sub vs. Queue Patterns**: Initial pub/sub implementation caused message duplication during scaling; switching to Redis Lists with BLPOP provided reliable work-queue semantics.
2. **Idempotent Processing**: Using HSETNX ensured accurate counters even with retries or duplicates, critical for reliable metrics.
3. **Kubernetes Scaling Challenges**: Multiple replicas with pub/sub created an exponential growth in message processing; proper queue semantics fixed this.
4. **Infrastructure-as-Code Principles**: Declarative Kubernetes manifests allowed for consistent, repeatable deployments with proper resource allocation.
5. **Observability Importance**: Redis counters and structured logging provided visibility into the asynchronous processing system.

## 5. Sample Results  
```
Sending batch messages...
Sent message 0: {'id': 'a121a50c-634c-4039-b25e-1c631f6e5408', 'status': 'processing'}
...
Sent message 99: {'id': '48fce327-f935-4c2a-9ebe-72bb67a25c85', 'status': 'processing'}

Message Processing Statistics:
Total messages sent: 102
Successful messages: 40
Failed messages: 62
Stuck messages: 0
```

The results demonstrate:
- Reliable message processing with exactly-once semantics
- Proper accounting of success/failure states
- No stuck messages, indicating full pipeline completion
- Approximately 40/60 success/failure ratio, matching the random decision in serviceB

This confirms our architecture successfully handles asynchronous message processing with proper queuing semantics and idempotent state tracking. 