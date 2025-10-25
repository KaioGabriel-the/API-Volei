from typing import Optional, List
from app.schemas.Partida import Partida, PartidaBase
from app.repository.PartidaRepository import PartidaRepository


class PartidaService:
    @staticmethod
    def listar_partidas() -> Optional[List[Partida]]:
        dados_partidas = PartidaRepository.get_all()

        if dados_partidas is None:
            return None
        
        partidas = [Partida(**i) for i in dados_partidas]

        return partidas
    

    @staticmethod
    def buscar_partida(id_partida: int) -> Optional[Partida]:
        dados_partida = PartidaRepository.get_by_id(id_partida)

        if dados_partida is None:
            return None
        
        return Partida(**dados_partida)
    

    @staticmethod
    def buscar_partidas_jogador(id_jogador: int) -> Optional[List[Partida]]:
        dados_partidas = PartidaRepository.get_by_id_jogador(id_jogador)

        if dados_partidas is None:
            return None
        
        partidas = [Partida(**i) for i in dados_partidas]

        return partidas
    

    @staticmethod
    def cadastrar_partida(nova_partida: PartidaBase) -> Optional[Partida]:
        partida_nova = nova_partida.model_dump()
        dados_nova_partida = PartidaRepository.create(partida_nova)

        return Partida(**dados_nova_partida)
    

    @staticmethod
    def atualizar_partida(id_partida: int, partida: PartidaBase) -> Optional[Partida]:
        partida_atualizada = partida.model_dump()
        dados_atualizados = PartidaRepository.update(id_partida, partida_atualizada)

        if dados_atualizados is None:
            return None
        
        return Partida(**dados_atualizados)
    

    @staticmethod
    def deletar_partida(id_partida: int) -> bool:
        partida_deletado = PartidaRepository.delete(id_partida)

        return partida_deletado
    