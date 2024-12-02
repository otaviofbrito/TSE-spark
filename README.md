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


