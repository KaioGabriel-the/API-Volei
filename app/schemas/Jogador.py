from pydantic import BaseModel, ConfigDict
from app.enums.jogador import Genero, Nivel, Posicao

class JogadorBase(BaseModel):
    nome: str
    idade: int
    genero: Genero.Genero
    posicao: Posicao.Poiscao
    nivel: Nivel.Nivel

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Leila Barros",
                "idade": 49,
                "genero": "FEMININO",
                "posicao": "OPOSTO",
                "nivel": "EXPERIENTE"
            }
        }


class Jogador(JogadorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)