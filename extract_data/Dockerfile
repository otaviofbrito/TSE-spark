# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o código-fonte para dentro do container
COPY . /app/extract_data

RUN pip install --no-cache-dir -r /app/extract_data/requirements.txt

# Comando para rodar o script
CMD ["python", "/app/extract_data/extract.py"]
