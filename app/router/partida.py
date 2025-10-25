from fastapi import APIRouter, status, HTTPException
from typing import Optional, List
from app.schemas.Partida import Partida, PartidaBase
from app.handlers.PartidaHandler import PartidaHandler


router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def partidas() -> Optional[List[Partida]]:
    lista_partidas = await PartidaHandler.listar()

    if lista_partidas is None:
        return None
    
    return lista_partidas


@router.get("/partida/{id_partida}", status_code=status.HTTP_200_OK)
async def partida(id_partida: int) -> Optional[Partida]:
    partida_buscada = await PartidaHandler.buscar(id_partida)

    if partida_buscada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A partida com o id {id_partida} não foi encontrada."
        )
    
    return partida_buscada


@router.get("/jogador/{id_jogador}")
async def partidas_jogador(id_jogador: int) -> Optional[List[Partida]]:
    pardidas_jogador = await PartidaHandler.buscar_partidas(id_jogador)

    if pardidas_jogador is None:
        return None
    
    return pardidas_jogador


@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_partida(nova_partida: PartidaBase) -> Optional[Partida]:
    partida_nova = await PartidaHandler.cadastrar(nova_partida)

    if partida_nova is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dados incompletos da partida. Não foi possível realizar o cadastrato."
        )
    
    return partida_nova


@router.put("/{id_partida}", status_code=status.HTTP_200_OK)
async def atualizar_partida(id_partida: int, novo_dado: PartidaBase) -> Optional[Partida]:
    partida_atualizada = await PartidaHandler.atualizar(id_partida, novo_dado)

    if partida_atualizada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partida com id {id_partida} não foi encontrada para atualização."
        )
    
    return partida_atualizada


@router.delete("/{id_partida}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_partida(id_partida: int):
    partida_deletada = await PartidaHandler.deletar(id_partida)

    if not partida_deletada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partida com id {id_partida} não foi encontrada para exclusão."
        )
