#!/bin/bash

# Build all Docker images
docker build -t servicefrontend:latest ./serviceFrontEnd
docker build -t servicea:latest ./serviceA
docker build -t serviceb:latest ./serviceB
docker build -t servicecomplete:latest ./serviceComplete

# Tag images for local registry (if using minikube or kind)
# Adjust as needed for your registry
if command -v minikube &> /dev/null; then
    eval $(minikube docker-env)
    docker build -t servicefrontend:latest ./serviceFrontEnd
    docker build -t servicea:latest ./serviceA
    docker build -t serviceb:latest ./serviceB
    docker build -t servicecomplete:latest ./serviceComplete
fi

# Apply K8s manifests in order
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-redis-configmap.yaml
kubectl apply -f k8s/02-logs-pvc.yaml
kubectl apply -f k8s/03-redis.yaml
kubectl apply -f k8s/04-serviceFrontEnd.yaml
kubectl apply -f k8s/05-serviceA.yaml
kubectl apply -f k8s/06-serviceB.yaml
kubectl apply -f k8s/07-serviceComplete.yaml
kubectl apply -f k8s/08-ingress.yaml

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl -n hsrn-vip wait --for=condition=available --timeout=180s deployment/redis
kubectl -n hsrn-vip wait --for=condition=available --timeout=180s deployment/servicefrontend
kubectl -n hsrn-vip wait --for=condition=available --timeout=180s deployment/servicea
kubectl -n hsrn-vip wait --for=condition=available --timeout=180s deployment/serviceb
kubectl -n hsrn-vip wait --for=condition=available --timeout=180s deployment/servicecomplete

echo "Deployment complete!"
kubectl -n hsrn-vip get all 