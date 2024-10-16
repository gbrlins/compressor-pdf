# Usar uma imagem base leve com Python
FROM registry.suse.com/bci/python:3.12

# Diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos necessários para o contêiner
COPY . .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir o ponto de entrada para o contêiner
ENTRYPOINT ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "compress_pdf:app"]
