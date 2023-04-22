from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec, Response
from pydantic import BaseModel

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
@spec.validate(resp=Response(HTTP_200=Pessoa))
def get_pessoas():
    return "Pessoas"

server.run()