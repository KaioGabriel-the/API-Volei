from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/{partida_id}")
async def read_convites(partida_id: int, status: Optional[str] = None):
    if status:
        return f"Lista de convites para a partida {partida_id} com status {status}"
    return f"Lista de todos os convites para a partida {partida_id}"


@router.post("/")
async def create_convite():
    return "Convite criado com sucesso"


@router.put("/{convite_id}/aceitar")
async def aceitar_convite(convite_id: int):
    return f"Convite com ID {convite_id} aceito com sucesso"


@router.put("/{convite_id}/recusar")
async def recusar_convite(convite_id: int):
    return f"Convite com ID {convite_id} recusado com sucesso"


@router.delete("/{convite_id}")
async def delete_convite(convite_id: int):
    return f"Convite com ID {convite_id} deletado com sucesso"
