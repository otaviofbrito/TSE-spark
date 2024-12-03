#!/bin/bash

##Volumes
kubectl apply -f ./k8s/volumes/pv.yaml
kubectl apply -f ./k8s/volumes/pvc.yaml

##Pods
kubectl apply -f ./k8s/pods/extract_data_pod.yaml
kubectl apply -f ./k8s/pods/streamlit_pod.yaml
kubectl apply -f ./k8s/pods/streamlit_service.yaml


##Spark Cluster
kubectl apply -f ./k8s/spark-master-deployment.yaml
kubectl apply -f ./k8s/spark-master-service.yaml
kubectl apply -f ./k8s/spark-worker-deployment.yaml