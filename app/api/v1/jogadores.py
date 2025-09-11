from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/")
async def read_jogadores():
    return "Lista de todos os jogadores"

@router.get("/")
async def read_jodadores(categoria: Optional[str] = None, genero: Optional[str] = None):
    return f"Lista de jogadores na categoria {categoria} ou gênero {genero}"

@router.get("/{jogador_id}")
async def read_jogador(jogador_id: int):
    return f"Detalhes do jogador com ID {jogador_id}"

@router.post("/")
async def create_jogador():
    return "Jogador criado com sucesso"

@router.put("/{jogador_id}")
async def update_jogador(jogador_id: int):
    return f"Jogador com ID {jogador_id} atualizado com sucesso"

@router.delete("/{jogador_id}")
async def delete_jogador(jogador_id: int):
    return f"Jogador com ID {jogador_id} deletado com sucesso"
