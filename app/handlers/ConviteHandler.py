from typing import Optional, List
from app.schemas.Convite import Convite, ConviteBase
from app.services.ConviteService import ConviteService

class ConviteHandler:

    @staticmethod
    async def listar() -> Optional[List[Convite]]:
        lista = ConviteService.listar_convites()
        
        return lista
    

    @staticmethod
    async def buscar(id_convite: int) -> Optional[Convite]:
        convite = ConviteService.buscar_convite(id_convite)

        return convite
    

    @staticmethod
    async def buscar_remetente(id_remetente: int) -> Optional[List[Convite]]:
        convites_remetente = ConviteService.buscar_convite_remente(id_remetente)

        return convites_remetente
    

    @staticmethod
    async def cadastrar(novo_convite: ConviteBase) -> Optional[Convite]:
        convite_criado = ConviteService.cadastrar_convite(novo_convite)

        return convite_criado
    

    @staticmethod
    async def atualizar(id_convite: int, convite: ConviteBase) -> Optional[Convite]:
        convite_atualizado = ConviteService.atualizar_convite(id_convite, convite)

        return convite_atualizado
    

    @staticmethod
    async def deletar(id_convite: int) -> bool:
        convite_deletado = ConviteService.deletar_convite(id_convite)

        return convite_deletado
    