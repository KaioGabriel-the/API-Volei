from typing import List, Optional
from app.schemas.Jogador import Jogador, JogadorBase
from app.repository.JogadorRepository import JogadorRepository

class JogadorService():
    @staticmethod
    def listar_jogadores() -> List[Jogador]:
        jogadores_dados = JogadorRepository.get_all()

        jogadores_formatados = [Jogador(**i) for i in jogadores_dados]

        return jogadores_formatados
    
    @staticmethod 
    def buscar_jogador(id_jogador : int) -> Optional[Jogador]:
        jogador_dado = JogadorRepository.get_by_id(id_jogador)
        
        if jogador_dado is None:
            return None
        
        jogador = Jogador(**jogador_dado)

        return jogador
    

    @staticmethod
    def cadastrar_jogador(novo_jogador:JogadorBase) -> Optional[Jogador]:
        jogador_dict = novo_jogador.model_dump()
        jogador = JogadorRepository.create(jogador_dict)

        return Jogador(**jogador)
    

    @staticmethod
    def deletar_jogador(id_jogador: int) -> bool:
        deletado = JogadorRepository.delete(id_jogador)
        return deletado
    

    @staticmethod
    def atualizar_jogador(id_jogador: int, jogador_data: JogadorBase) -> Optional[Jogador]:
        data_dict = jogador_data.model_dump()
        
        jogador_atualizado_dict = JogadorRepository.update(id_jogador, data_dict)
        
        if jogador_atualizado_dict is None:
            return None 
        
        return Jogador(**jogador_atualizado_dict)