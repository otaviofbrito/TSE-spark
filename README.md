minikube start --cpus=6 --memory=8g
minikube ssh
sudo mkdir -p /mnt/data/Volumes/raw/tse
sudo mkdir -p /mnt/data/Volumes/silver/tse
sudo mkdir -p /mnt/data/Volumes/gold/tse


eval $(minikube docker-env)

docker build -t my-extract-data-image .




kubectl exec -it spark-master-9846cfc54-k78xh -- spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --conf spark.driver.bindAddress=spark-master \
  --conf spark.driver.host=spark-master \
  /app/spark/pyspark/consulta_cand_raw.py

  kubectl exec -it spark-master-9846cfc54-k78xh -- spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --conf spark.driver.bindAddress=spark-master \
  --conf spark.driver.host=spark-master \
  /app/spark/pyspark/consulta_bem_raw.py


kubectl exec -it spark-master-9846cfc54-k78xh -- spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --conf spark.driver.bindAddress=spark-master \
  --conf spark.driver.host=spark-master \
  /app/spark/pyspark/consolidate_bem_cand_agg_value.py

#!/bin/bash

# Encontra o nome do pod do Spark Master automaticamente
SPARK_MASTER_POD=$(kubectl get pods -l app=spark,component=master -o jsonpath='{.items[0].metadata.name}')

# Executa o spark-submit com o nome do pod do master
kubectl exec -it "$SPARK_MASTER_POD" -- spark-submit \
  --master spark://spark-master-service:7077 \
  --deploy-mode client \
  --conf spark.driver.bindAddress=spark-master-service \
  --conf spark.driver.host=spark-master-service \
  /app/spark/pyspark/consulta_cand_raw.py



http://localhost:8501