#!/bin/bash

kubectl apply -f ./k8s/spark-master-deployment.yaml
kubectl apply -f ./k8s/spark-master-service.yaml
kubectl apply -f ./k8s/spark-workers-deployment.yaml
