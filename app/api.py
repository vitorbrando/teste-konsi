import requests
from fastapi import FastAPI
import app.crawler as crawler
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
tokens_cache = {}

class Consulta(BaseModel):
    cpf: str
    usuario: str
    senha: str

@app.post("/beneficios")
async def beneficios(consulta: Consulta) -> dict:
    global tokens_cache
    if tokens_cache.get(consulta.usuario) == None:
        tokens_cache[consulta.usuario] = crawler.get_auth_token(consulta.usuario, consulta.senha)
    
    URL_EXTRATO = os.getenv('URL_EXTRATO')    
    endpoint = "{}{}{}{}".format("http://", URL_EXTRATO, "/offline/listagem/", consulta.cpf)
    headers = {"Authorization": tokens_cache[consulta.usuario]}

    resp = requests.get(endpoint, headers=headers)
    if resp.status_code == 200:
        resp_json = resp.json()
        if len(resp_json['beneficios']) > 1:
            nb = []
            for b in resp_json['beneficios']:
                nb.append(b['nb'])
        else:
            nb = (resp.json()['beneficios'][0]['nb'])
        return {"result": nb}
    else:
        tokens_cache[consulta.usuario] = None
        return {"result": "falha ao consultar cpf"}
