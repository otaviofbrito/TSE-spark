# 🗳️ Coleta e Processamento de Dados de Candidatos - Eleições 2024 

## Descrição do Projeto

Este projeto tem como objetivo coletar dados sobre os candidatos das eleições de 2024, processá-los de forma distribuída utilizando o Apache Spark e Kubernetes, e, por fim, disponibilizar uma página interativa no **Streamlit** com análises e gráficos baseados nos dados processados. O objetivo final é fornecer uma plataforma visual para análise dos dados dos candidatos.

## Tecnologias Utilizadas 🛠️

- **Kubernetes**: Orquestração de containers para escalabilidade e gerenciamento de recursos.
- **Minikube**: Ferramenta para rodar o Kubernetes localmente.
- **Apache Spark**: Processamento de grandes volumes de dados de forma distribuída.
- **PySpark**: Interface Python para o Apache Spark.
- **Docker**: Containerização das aplicações para facilitar o desenvolvimento e a implantação.
- **Streamlit**: Framework para criar interfaces interativas com Python (utilizando Pandas e Plotly para análise de dados e visualizações).

## Requisitos 📋

Antes de rodar o projeto, você precisará instalar e configurar os seguintes componentes:

- **Minikube**: [Instalação do Minikube](https://minikube.sigs.k8s.io/docs/)
- **Docker**: [Instalação do Docker](https://docs.docker.com/get-docker/)

## Fonte de Dados :floppy_disk:

- :link: **Dataset de Candidatos 2024**: [Dados Abertos TSE 2024](https://dadosabertos.tse.jus.br/dataset/candidatos-2024) 

## Execução 🚀

1. **Iniciar o Minikube**:
   Primeiro, inicie o Minikube com os seguintes parâmetros para alocar recursos suficientes para os pods do Kubernetes:

   ```bash
   minikube start --cpus=6 --memory=8g
   ```

2. **Acessar o Minikube**:

   Após iniciar o Minikube, faça login no ambiente SSH:

   ```bash
   minikube ssh
   ```

3. **Criar Volume no Minikube**:

   Crie os diretórios necessários para armazenar volumes persistentes:

   ```bash
   sudo mkdir -p /mnt/data/Volumes
   ```

4. **Configuração do Docker**:

   Execute o comando abaixo para configurar o Docker para rodar no Minikube:

   ```bash
   eval $(minikube docker-env)
   ```

5. **Construir as Imagens Docker**:

   Construa as imagens Docker para os três componentes principais: **Extração de Dados**, **Streamlit** e **Spark**.

   ```bash
   docker build -t my-extract-data-image ./extract_data
   docker build -t my-streamlit-image ./streamlit
   docker build -t my-spark-image ./spark
   ```

6. **Permissões de Execução**:

   Torne os scripts executáveis:

   ```bash
   chmod +x run_jobs.sh
   chmod +x create.sh
   chmod +x delete.sh
   ```

7. **Acessar o Dashboard do Kubernetes**:

   Inicie o dashboard do Kubernetes:

   ```bash
   minikube dashboard
   ```

8. **Criar os Recursos no Kubernetes**:

   Para iniciar os pods, serviços, deploys, PV e PVC no Kubernetes, execute o script abaixo:

   ```bash
   ./create.sh
   ```

9. **Deletar os Recursos no Kubernetes**:

   Para deletar todos os recursos iniciados, execute:

   ```bash
   ./delete.sh
   ```

10. **Executar os Scripts de Processamento de Dados**:

    Para processar os dados utilizando o Spark, execute o seguinte script:

    ```bash
    ./run_jobs.sh
    ```

## Acessando a Aplicação 🌐

Após a execução dos passos acima, você pode acessar as seguintes URLs:

- **Spark UI**: Interface do Apache Spark para monitorar o processamento dos dados.
  - `http://<minikubeip>:30001`

- **Streamlit Dashboard**: Interface interativa para visualização das análises e gráficos.
  - `http://<minikubeip>:30099`

Para obter o endereço IP do Minikube, execute o comando:

```bash
minikube ip
```