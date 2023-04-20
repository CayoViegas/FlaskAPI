from flask import Flask

server = Flask(__name__)

@server.get("/pessoas")
def get_pessoas():
    return "Pessoas"