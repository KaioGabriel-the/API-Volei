from enums.jogador import Categoria, Genero
from pydantic import BaseModel


class JogadorCreate(BaseModel):
    nome: str
    categoria: Categoria
    genero: Genero
    idade: int
    posicao: str
    email: str

class JogadorResponse(BaseModel):
    message: str
    jogador: JogadorCreate
