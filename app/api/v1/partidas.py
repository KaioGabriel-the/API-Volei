from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_partidas():
    return "Lista de todas as partidas"

@router.get("/{partida_id}")
async def read_partida(partida_id: int):
    return f"Detalhes da partida com ID {partida_id}"

@router.post("/")
async def create_partida():
    return "Partida criada com sucesso"

@router.put("/{partida_id}")
async def update_partida(partida_id: int):
    return f"Partida com ID {partida_id} atualizada com sucesso"

@router.delete("/{partida_id}")
async def delete_partida(partida_id: int):
    return f"Partida com ID {partida_id} deletada com sucesso"

