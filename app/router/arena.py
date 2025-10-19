from fastapi import APIRouter, status, HTTPException
from typing import List
from app.handlers.ArenaHandler import ArenaHandler
from app.schemas.Arena import Arena, ArenaBase

router = APIRouter()

@router.get("/", status_code=200, response_model=List[Arena])
async def arenas() -> List[Arena]:
    list_arena = await ArenaHandler.listar()
    if list_arena is None:
        return []

    return list_arena


@router.get("/{id_arena}", status_code=200, response_model=Arena)
async def arena(id_arena: int) -> Arena:
    arena_encontrada = await ArenaHandler.buscar(id_arena)

    if arena_encontrada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arena com id {id_arena} não encontrada."
        )
    
    return arena_encontrada


@router.post("/", status_code=201, response_model=Arena)
async def cadastrar_arena(nova_arena:ArenaBase):
    dados_arena = await ArenaHandler.cadastrar(nova_arena)

    if dados_arena is HTTPException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dados incompletos da arena. Não foi possível realizar o cadastrato."
        )
    
    return dados_arena


@router.delete("/{id_arena}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_arena(id_arena: int):
    deletado = await ArenaHandler.deletar(id_arena)

    if not deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arena com id {id_arena} não encontrada para exclusão."
        )
    
    return


@router.put("/{id_arena}", status_code=status.HTTP_200_OK, response_model=Arena)
async def atualizar_arena(id_arena: int, arena_data: ArenaBase):
    arena_atualizado = await ArenaHandler.atualizar(id_arena, arena_data)
    
    if arena_atualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arena com id {id_arena} não encontrada para atualização."
        )
    
    return arena_atualizado
