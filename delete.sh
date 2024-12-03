#!/bin/bash

##Volumes
kubectl delete -f ./k8s/volumes/pv.yaml
kubectl delete -f ./k8s/volumes/pvc.yaml

##Pods
kubectl delete -f ./k8s/pods/extract_data_pod.yaml
kubectl delete -f ./k8s/pods/streamlit_pod.yaml
kubectl delete -f ./k8s/pods/streamlit_service.yaml


##Spark Cluster
kubectl delete -f ./k8s/spark-master-deployment.yaml
kubectl delete -f ./k8s/spark-master-service.yaml
kubectl delete -f ./k8s/spark-worker-deployment.yaml

