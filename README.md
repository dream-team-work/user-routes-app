### PROJETO TIVIT AVALIACAO DE PERFORMACE DE TRABALHO

### Fomas de executar o projeto:

Subindo todo o projeto para testes.
```
docker-compose up
```

### Subindo o projeto via VS code para testes com modo debug ( *** APENAS PARA DESENVOLVIMENTO BACKEND *** )
Crie um ambiente virtual no Terminal do VS Code:
```
python -m venv venv
```
E depois ative o ambiente no CMD:
```
venv\Scripts\activate 
```

Instale as dependencias
```
pip install -r requirements.txt
```

Criando o banco de dados via docker: ( DETALHE NA PORTA DO HOST QUE FICOU 5433 )
```
docker run --name postgres-container -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5433:5432 -d postgres
```

E para rodar o projeto use:
```
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```