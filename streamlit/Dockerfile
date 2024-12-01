# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o código-fonte para dentro do container
COPY . /app/streamlit

# Instale as dependências (se houver)
RUN pip install --no-cache-dir -r /app/streamlit/requirements.txt

# Comando para rodar o script
CMD ["streamlit", "run", "/app/streamlit/app.py"]
