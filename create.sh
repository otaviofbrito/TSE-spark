#!/bin/bash

# kubectl apply -f ./k8s/spark-master-deployment.yaml
# kubectl apply -f ./k8s/spark-master-service.yaml
# kubectl apply -f ./k8s/spark-workers-deployment.yaml


##Volumes
kubectl apply -f ./k8s/volumes/raw/pv-raw.yaml
kubectl apply -f ./k8s/volumes/raw/pvc-raw.yaml

kubectl apply -f ./k8s/volumes/silver/pv-silver.yaml
kubectl apply -f ./k8s/volumes/silver/pvc-silver.yaml

kubectl apply -f ./k8s/volumes/gold/pv-gold.yaml
kubectl apply -f ./k8s/volumes/gold/pvc-gold.yaml

##Pods
kubectl apply -f ./k8s/pods/extract_data_pod.yaml
kubectl apply -f ./k8s/pods/streamlit_pod.yaml
