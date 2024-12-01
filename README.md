minikube start --cpus=6 --memory=8g
minikube ssh
sudo mkdir -p /mnt/data/Volumes/raw/tse
sudo mkdir -p /mnt/data/Volumes/silver/tse
sudo mkdir -p /mnt/data/Volumes/gold/tse


eval $(minikube docker-env)

docker build -t my-extract-data-image .


