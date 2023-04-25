import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_ENDERECOS_TABLE = """CREATE TABLE IF NOT EXISTS Enderecos (
                               id SERIAL PRIMARY KEY,
                               logradouro VARCHAR(100) NOT NULL,
                               cep CHAR(8) NOT NULL,
                               numero INTEGER NOT NULL,
                               cidade VARCHAR(100) NOT NULL
                            );"""

CREATE_PESSOAS_TABLE = """CREATE TABLE IF NOT EXISTS Pessoas (
                             id SERIAL PRIMARY KEY,
                             nome VARCHAR(100) NOT NULL,
                             data_nascimento DATE NOT NULL,
                             endereco_id INTEGER REFERENCES Enderecos(id)
                          );"""

INSERT_PESSOA = """INSERT INTO Pessoas (nome, data_nascimento, endereco_id)
                   VALUES (%s, %s, %s)
                   RETURNING id;"""

INSERT_ENDERECO = """INSERT INTO Enderecos (logradouro, cep, numero, cidade)
                     VALUES (%s, %s, %s, %s)
                     RETURNING id;"""
                             
load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/pessoa")
def criar_pessoa():
    data = request.get_json()
    nome = data["nome"]
    data_nascimento = data["data_nascimento"]
    logradouro = data["logradouro"]
    cep = data["cep"]
    numero = data["numero"]
    cidade = data["cidade"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ENDERECOS_TABLE)
            cursor.execute(CREATE_PESSOAS_TABLE)
            cursor.execute(INSERT_ENDERECO, (logradouro, cep, numero, cidade))
            id_endereco = cursor.fetchone()[0]
            cursor.execute(INSERT_PESSOA, (nome, data_nascimento, id_endereco))
            id_pessoa = cursor.fetchone()[0]
    
    return {"id": id_pessoa, "message": "Pessoa criada com sucesso."}, 201