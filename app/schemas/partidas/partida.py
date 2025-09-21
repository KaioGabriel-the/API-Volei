from pydantic import BaseModel
from app.enums.jogador import Categoria, Genero
from app.enums.partida import StatusPartida
from app.schemas.convites.convite import Convite

class PartidaCreate(BaseModel):
    id_criador: int
    categoria: Categoria
    idade_minima: int
    idade_maxima: int
    genero: Genero
    status: StatusPartida
    covites: list[Convite] = []
