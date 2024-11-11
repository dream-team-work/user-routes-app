### PROJETO TIVIT AVALIACAO DE PERFORMACE DE TRABALHO

### Fomas de executar o projeto:

Subindo todo o projeto para testes.
```
docker-compose up
```

### Subindo o projeto via VS code para testes com modo debug ( *** APENAS PARA DESENVOLVIMENTO BACKEND *** )

1°) Criando o banco de dados via docker:
```
docker run --name postgres-container -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5432:5432 -d postgres
```


2°) Crie um ambiente virtual no Terminal do VS Code:
```
python -m venv venv
```

3°) E depois ative o ambiente no CMD:
```
source venv/bin/activate
```
4°) E para rodar o projeto use:
```
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

