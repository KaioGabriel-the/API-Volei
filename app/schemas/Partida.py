from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from app.enums.jogador import Nivel

class PartidaBase(BaseModel):
    id_criador: int
    id_arena: int

    limite_max: Optional[int] = None
    limite_min: Optional[int] = None
    idade_min: Optional[int] = None
    categoria: Optional[Nivel.Nivel] = None

    jogadores: List[int] = Field(default_factory=list)

    # 🔍 Validação: idade_min positiva
    @field_validator("idade_min")
    def idade_min_nao_negativa(cls, v):
        if v is not None and v < 0:
            raise ValueError("idade_min não pode ser negativa")
        return v

    # 🔍 Validação: jogadores sem duplicados
    @field_validator("jogadores")
    def validar_jogadores(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("A lista de jogadores não pode conter IDs duplicados")
        return v

    # 🔍 Validação entre campos: limite_max >= limite_min
    @model_validator(mode="before")
    def validar_limites(cls, values):
        limite_min = values.get("limite_min")
        limite_max = values.get("limite_max")
        if limite_min is not None and limite_max is not None and limite_min > limite_max:
            raise ValueError("limite_min não pode ser maior que limite_max")
        return values

class Partida(PartidaBase):
    id_partida: int

    model_config = ConfigDict(from_attributes=True)
