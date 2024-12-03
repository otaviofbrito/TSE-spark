#!/bin/bash

# Encontrar o nome do pod do Spark Master automaticamente
echo "Localizando o pod do Spark Master..."
SPARK_MASTER_POD=$(kubectl get pods -l app=spark,role=master -o jsonpath='{.items[0].metadata.name}')

# Verificar se encontrou o pod do Spark Master
if [ -z "$SPARK_MASTER_POD" ]; then
  echo "Erro: Não foi possível encontrar o pod do Spark Master. Verifique se o pod está em execução."
  exit 1
fi

echo "Pod do Spark Master encontrado: $SPARK_MASTER_POD"

# Função para executar o spark-submit no pod do Spark Master
execute_spark_job() {
  local script_path=$1
  echo "Executando job: $script_path"
  kubectl exec -it "$SPARK_MASTER_POD" -- spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    --conf spark.driver.bindAddress=spark-master \
    --conf spark.driver.host=spark-master \
    "$script_path"
  
  # Verificar se o comando spark-submit foi bem-sucedido
  if [ $? -eq 0 ]; then
    echo "Job $script_path finalizado com sucesso!"
  else
    echo "Erro ao executar o job: $script_path"
    exit 1
  fi
}

# Executar os jobs
execute_spark_job "/app/spark/pyspark/consulta_cand_raw.py"
execute_spark_job "/app/spark/pyspark/consulta_bem_raw.py"
execute_spark_job "/app/spark/pyspark/consolidate_bem_cand_agg_value.py"

echo "Todos os jobs foram executados com sucesso!"
