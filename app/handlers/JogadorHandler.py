from typing import List, Optional
from app.schemas import Jogador
from app.services.JogadorService import JogadorService


class JogadorHandler:

    @staticmethod
    async def listar() -> List[Jogador.Jogador]:
        lista_jogadores = JogadorService.listar_jogadores()

        return lista_jogadores
    
    @staticmethod
    async def buscar(id_jogador : int) -> Optional[Jogador.Jogador]:
        jogador = JogadorService.buscar_jogador(id_jogador)

        if jogador is None:
            return None
        
        return jogador
    
    @staticmethod
    async def cadastrar(novo_jogador : Jogador.JogadorBase) -> Optional[Jogador.Jogador]:
        jogador = JogadorService.cadastrar_jogador(novo_jogador)

        return jogador
    

    @staticmethod
    async def deletar(id_jogador: int) -> bool:
        deletado = JogadorService.deletar_jogador(id_jogador)
        return deletado
    

    @staticmethod
    async def atualizar(id_jogador: int, jogador_data: Jogador.JogadorBase) -> Optional[Jogador.Jogador]:
        
        jogador_atualizado = JogadorService.atualizar_jogador(id_jogador, jogador_data)
        return jogador_atualizado