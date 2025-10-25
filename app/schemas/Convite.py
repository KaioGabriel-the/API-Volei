from pydantic import BaseModel, ConfigDict
from app.enums.convite import Status


class ConviteBase(BaseModel):
    id_remetente: int
    id_partida: int
    status: Status.Status


class Convite(ConviteBase):
    id_convite: int

    model_config = ConfigDict(from_attributes=True)
