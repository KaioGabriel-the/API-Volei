from fastapi import FastAPI
from app.routers.jogadores_router import router as jogadores_router
from app.routers.partidas_router import router as partidas_router
from app.routers.convites_router import router as convites_router
from app.routers.auth_router import router as auth_router

app = FastAPI()

app.include_router(jogadores_router, prefix="/jogadores", tags=["jogadores"])
app.include_router(partidas_router, prefix="/partidas", tags=["partidas"])
app.include_router(convites_router, prefix="/convites", tags=["convites"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])