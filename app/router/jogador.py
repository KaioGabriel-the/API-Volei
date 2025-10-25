from fastapi import APIRouter, status, HTTPException
from typing import Optional, List
from app.schemas import Jogador
from app.handlers.JogadorHandler import JogadorHandler

router = APIRouter()

@router.get("/",status_code=200)
async def jogadores() -> Optional[List[Jogador.Jogador]]:
    list_jogador = await JogadorHandler.listar()
    if list_jogador is None:
        return None
    
    return list_jogador


@router.get("/{id_jogador}",status_code=200)
async def jogador(id_jogador : int):
    jogador = await JogadorHandler.buscar(id_jogador)

    if jogador is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogador com id {id_jogador} não encontrado."
        )
    
    return jogador


@router.post("/", status_code=201, response_model= Jogador.Jogador)
async def criar_jogador(novo_jogador: Jogador.JogadorBase):
    dados_jogador = await JogadorHandler.cadastrar(novo_jogador)

    if dados_jogador is HTTPException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dados incompletos do jogador. Não foi possível realizar o cadastrato."
        )
    
    return dados_jogador


@router.delete("/{id_jogador}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_jogador(id_jogador: int):
    deletado = await JogadorHandler.deletar(id_jogador)

    if not deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogador com id {id_jogador} não encontrado para exclusão."
        )
    
    return


@router.put(
    "/{id_jogador}", 
    status_code=status.HTTP_200_OK, 
    response_model=Jogador.Jogador 
)
async def atualizar_jogador(id_jogador: int, jogador_data: Jogador.JogadorBase):
    jogador_atualizado = await JogadorHandler.atualizar(id_jogador, jogador_data)
    
    if jogador_atualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogador com id {id_jogador} não encontrado para atualização."
        )
    
    return jogador_atualizado
