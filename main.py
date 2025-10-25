from fastapi import FastAPI
from app.router import jogador, arena, convite, partida

app = FastAPI()

app.include_router(jogador.router, prefix="/jogadores", tags=["Jogador"])
app.include_router(arena.router, prefix="/arenas", tags=["Arena"])
app.include_router(convite.router, prefix="/convites", tags=["Convite"])
app.include_router(partida.router, prefix="/partidas", tags=["Partida"])

@app.get("/")
def hello_world():
    return {"message": "Bem-vindo à API de Jogadores!"}