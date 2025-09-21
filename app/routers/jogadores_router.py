from fastapi import APIRouter, HTTPException
from typing import Optional
from app.schemas.jogadores.jogador import JogadorCreate, JogadorResponse, Jogador
from app.services.JagadorService import JogadorService

router = APIRouter()

@router.get("/", response_model=list[Jogador], status_code=200)
async def read_jogadores() -> list[Jogador]:
    try:
        return JogadorService.get_all_jogadores()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[Jogador], status_code=200)
async def read_jodadores(categoria: Optional[str] = None, genero: Optional[str] = None):
    try:
        if categoria and genero:
            return JogadorService.get_jogadores_by_categoria_and_genero(categoria, genero)
        elif categoria:
            return JogadorService.get_jogadores_by_categoria(categoria)
        elif genero:
            return JogadorService.get_jogadores_by_genero(genero)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{jogador_id}",response_model= Jogador, status_code=200)
async def read_jogador(jogador_id: int):
    try:
        return JogadorService.get_jogador_by_id(jogador_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id_jogador}/avaliacoes")
async def get_avaliacoes(id_jogador: int):
    return f"Lista de avaliações para o jogador com ID {id_jogador}"


@router.post("/", response_model=JogadorResponse,  status_code=201)
async def create_jogador(jogador: JogadorCreate) -> JogadorResponse:
    try:
        return JogadorService.create_jogador(jogador)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id_jogador}/avaliacoes")
async def avaliar_jogador(id_jogador: int, nota: int):
    return f"Jogador com ID {id_jogador} avaliado com nota {nota}"


@router.put("/{jogador_id}")
async def update_jogador(jogador_id: int):
    return f"Jogador com ID {jogador_id} atualizado com sucesso"


@router.delete("/{jogador_id}", status_code=204)
async def delete_jogador(jogador_id: int):
    try:
        JogadorService.delete_jogador(jogador_id)
        return {"message": "Jogador deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
