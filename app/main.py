from fastapi import FastAPI
from app.api.v1.jogadores import router as jogadores_router
from app.api.v1.partidas import router as partidas_router

app = FastAPI()

app.include_router(jogadores_router, prefix="/jogadores", tags=["jogadores"])
app.include_router(partidas_router, prefix="/partidas", tags=["partidas"])
