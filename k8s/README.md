# Kubernetes Deployment Guide

This directory contains Kubernetes manifests for deploying the message processing pipeline.

## Prerequisites

- Kubernetes cluster (Minikube, kind, EKS, GKE, AKS, etc.)
- kubectl configured to access your cluster
- Docker to build container images

## Quick Start

1. **Build and deploy everything at once:**

   ```bash
   ./deploy-to-k8s.sh
   ```

2. **Apply manifests manually:**

   ```bash
   # Create namespace
   kubectl apply -f k8s/00-namespace.yaml
   
   # Apply ConfigMap and PVC
   kubectl apply -f k8s/01-redis-configmap.yaml
   kubectl apply -f k8s/02-logs-pvc.yaml
   
   # Deploy Redis
   kubectl apply -f k8s/03-redis.yaml
   
   # Deploy microservices
   kubectl apply -f k8s/04-serviceFrontEnd.yaml
   kubectl apply -f k8s/05-serviceA.yaml
   kubectl apply -f k8s/06-serviceB.yaml
   kubectl apply -f k8s/07-serviceComplete.yaml
   
   # Apply Ingress (if your cluster supports it)
   kubectl apply -f k8s/08-ingress.yaml
   ```

## Testing the Deployment

1. **If using Minikube:**

   ```bash
   # Get the service URL
   FRONTEND_URL=$(minikube service -n hsrn-vip servicefrontend --url)
   
   # Run the test script
   ./k8s-test-script.py --host=$(echo $FRONTEND_URL | cut -d'/' -f3 | cut -d':' -f1) --port=$(echo $FRONTEND_URL | cut -d':' -f3)
   ```

2. **If using a cloud provider with LoadBalancer or Ingress:**

   ```bash
   # Get the external IP 
   FRONTEND_IP=$(kubectl -n hsrn-vip get svc servicefrontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
   
   # Run the test script
   ./k8s-test-script.py --host=$FRONTEND_IP --port=80
   ```

3. **Port forwarding (works with any cluster):**

   ```bash
   # Forward the Redis port
   kubectl -n hsrn-vip port-forward svc/redis 6379:6379 &
   
   # Forward the serviceFrontEnd port
   kubectl -n hsrn-vip port-forward svc/servicefrontend 8080:5000 &
   
   # Run the test with local ports
   ./k8s-test-script.py --host=localhost --port=8080 --redis-host=localhost --redis-port=6379
   ```

## Scaling Considerations

The microservices use Redis Lists to implement a work queue pattern:

```bash
# Scale services as needed
kubectl -n hsrn-vip scale deployment servicea serviceb servicecomplete --replicas=2

# For high throughput scenarios, scale serviceB which does the most processing
kubectl -n hsrn-vip scale deployment serviceb --replicas=3
```

Note that due to the work queue pattern implementation, you can safely scale the services without causing message duplication. Each message will be processed exactly once regardless of how many replicas are running.

## Monitoring

Check pod status:
```bash
kubectl -n hsrn-vip get pods
```

View logs from a specific service:
```bash
kubectl -n hsrn-vip logs -l app=servicefrontend
kubectl -n hsrn-vip logs -l app=servicea
kubectl -n hsrn-vip logs -l app=serviceb
kubectl -n hsrn-vip logs -l app=servicecomplete
```

Check the HPA status:
```bash
kubectl -n hsrn-vip get hpa serviceb-hpa
```

## Cleanup

Remove everything:
```bash
kubectl delete namespace hsrn-vip
``` 