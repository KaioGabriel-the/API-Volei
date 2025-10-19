from pydantic import BaseModel, ConfigDict

class ArenaBase(BaseModel):
    nome: str
    enderecao: str
    valor_hora: float
    qtd_jogadores: int


class Arena(ArenaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)