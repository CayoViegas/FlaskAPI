from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
import psycopg2

con = psycopg2.connect(host="localhost",
                       database="flaskapi", 
                       user="asd", 
                       password="123")

cur = con.cursor()

server = Flask(__name__)
spec = FlaskPydanticSpec("Flask", title="FlaskAPI")
spec.register(server)

class Endereco(BaseModel):
    id: int
    logradouro: str
    cep: str
    numero: int
    cidade: str

class Pessoa(BaseModel):
    id: int
    nome: str
    data_nascimento: str
    endereco: Endereco

@server.get("/pessoas")
def get_pessoas():
    return "Pessoas"

@server.post("/pessoas")
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def criar_pessoa():
    body = request.context.body.dict()
    return body


server.run()