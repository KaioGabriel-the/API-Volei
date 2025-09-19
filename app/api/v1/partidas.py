from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/")
async def read_partidas():
    return "Lista de todas as partidas"

@router.get("/")
async def read_partidas(genero: Optional[str] = None, categoria: Optional[str] = None):
    if genero:
        return f"Lista de partidas do gênero: {genero}"
    if categoria:
        return f"Lista de partidas da categoria: {categoria}"
    return "Lista de todas as partidas"

@router.get("/{partida_id}")
async def read_partida(partida_id: int):
    return f"Detalhes da partida com ID {partida_id}"


@router.get("/{partida_id}/jogadores")
async def get_jogadores(partida_id: int):
    return f"Lista de jogadores para a partida com ID {partida_id}"


@router.get("/{partida_id}/avaliacoes")
async def get_avaliacoes(partida_id: int):
    return f"Lista de avaliações para a partida com ID {partida_id}"

@router.post("/")
async def create_partida():
    return "Partida criada com sucesso"

@router.post("/{partida_id}/avaliacoes")
async def avaliar_partida(partida_id: int, nota: int):
    return f"Partida com ID {partida_id} avaliada com nota {nota}"

@router.put("/{partida_id}")
async def update_partida(partida_id: int):
    return f"Partida com ID {partida_id} atualizada com sucesso"

@router.delete("/{partida_id}")
async def delete_partida(partida_id: int):
    return f"Partida com ID {partida_id} deletada com sucesso"
