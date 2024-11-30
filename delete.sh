#!/bin/bash

kubectl delete -f ./k8s/spark-master-deployment.yaml
kubectl delete -f ./k8s/spark-master-service.yaml
kubectl delete -f ./k8s/spark-workers-deployment.yaml