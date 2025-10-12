from fastapi import FastAPI
from app.router import jogador

app = FastAPI()

app.include_router(jogador.router, prefix="/jogadores", tags=["jogadores"])

@app.get("/")
def hello_world():
    return {"message": "Bem-vindo à API de Jogadores!"}