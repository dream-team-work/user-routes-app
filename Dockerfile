# Use Python 3.10 como base
FROM python:3.10

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/

# Criar o ambiente virtual
RUN python -m venv /opt/venv

# Ativar o ambiente virtual
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Instalar as dependências dentro do ambiente virtual
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar o código da aplicação para o container
COPY ./ /app/

# Instalar o Uvicorn (servidor ASGI recomendado para FastAPI)
RUN pip install uvicorn

# Expor a porta 8000 para que o FastAPI esteja acessível
EXPOSE 8000

# Comando para rodar a aplicação FastAPI com uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]




