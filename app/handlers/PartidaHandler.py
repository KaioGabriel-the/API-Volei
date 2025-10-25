from typing import Optional, List
from app.schemas.Partida import Partida, PartidaBase
from app.services.PartidaService import PartidaService


class PartidaHandler:
    @staticmethod
    async def listar() -> Optional[List[Partida]]:
        lista = PartidaService.listar_partidas()
        
        return lista
    

    @staticmethod
    async def buscar(id_partida: int) -> Optional[Partida]:
        partida = PartidaService.buscar_partida(id_partida)

        return partida
    

    @staticmethod
    async def buscar_partidas(id_jogador: int) -> Optional[List[Partida]]:
        convites_remetente = PartidaService.buscar_partidas_jogador(id_jogador)

        return convites_remetente
    

    @staticmethod
    async def cadastrar(nova_partida: PartidaBase) -> Optional[Partida]:
        partida_criada = PartidaService.cadastrar_partida(nova_partida)

        return partida_criada
    

    @staticmethod
    async def atualizar(id_partida: int, partida: PartidaBase) -> Optional[Partida]:
        partida_atualizada = PartidaService.atualizar_partida(id_partida, partida)

        return partida_atualizada
    

    @staticmethod
    async def deletar(id_partida: int) -> bool:
        partida_deletada = PartidaService.deletar_partida(id_partida)

        return partida_deletada
    