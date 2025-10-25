from fastapi import APIRouter, status, HTTPException
from typing import Optional, List
from app.schemas.Convite import Convite, ConviteBase
from app.handlers.ConviteHandler import ConviteHandler

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def convites() -> Optional[List[Convite]]:
    lista_convites = await ConviteHandler.listar()

    if lista_convites is None:
        return None
    
    return lista_convites


@router.get("/convite/{id_convite}", status_code=status.HTTP_200_OK)
async def convite(id_convite: int) -> Optional[Convite]:
    convite_buscado = await ConviteHandler.buscar(id_convite)

    if convite_buscado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Convite com id {id_convite} não encontrado."
        )
    
    return convite_buscado


@router.get("/remetente/{id_remetente}", status_code=status.HTTP_200_OK)
async def convites_remente(id_remetente: int) -> Optional[List[Convite]]:
    lista_rementes = await ConviteHandler.buscar_remetente(id_remetente)

    if lista_rementes is None:
        return None
    
    return lista_rementes


@router.post("/",status_code=201)
async def enviar_convite(novo_convite: ConviteBase) -> Optional[Convite]:
    convite_cadastrado = await ConviteHandler.cadastrar(novo_convite)

    if convite_cadastrado is HTTPException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dados incompletos do convite. Não foi possível realizar o cadastrato."
        )
    
    return convite_cadastrado


@router.put("/{id_convite}", status_code=status.HTTP_200_OK)
async def atualizar_convite(id_convite: int, convite: ConviteBase) -> Optional[Convite]:
    convite_atualizado = await ConviteHandler.atualizar(id_convite, convite)

    if convite_atualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Convite com id {id_convite} não encontrado para atualização."
        )
    
    return convite_atualizado


@router.delete("/{id_convite}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_convite(id_convite: int):
    convite_deletado = await ConviteHandler.deletar(id_convite) 

    if not convite_deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Convite com id {id_convite} não encontrado para exclusão."
        )

    return