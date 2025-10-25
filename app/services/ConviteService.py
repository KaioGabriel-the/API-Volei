from typing import Optional, List
from app.schemas.Convite import Convite, ConviteBase
from app.repository.ConviteRepository import ConviteRepository

class ConviteService:

    @staticmethod
    def listar_convites() -> Optional[List[Convite]]:
        dados_convites = ConviteRepository.get_all()

        if dados_convites is None:
            return None
        
        convites = [Convite(**i) for i in dados_convites]

        return convites
    

    @staticmethod
    def buscar_convite(id_convite: int) -> Optional[Convite]:
        dados_convite = ConviteRepository.get_by_id(id_convite)

        if dados_convite is None:
            return None
        
        return Convite(**dados_convite)
    

    @staticmethod
    def buscar_convite_remente(id_remetente: int) -> Optional[List[Convite]]:
        dados_remetente = ConviteRepository.get_by_id_remetente(id_remetente)

        if dados_remetente is None:
            return None
        
        convites = [Convite(**i) for i in dados_remetente]

        return convites
    

    @staticmethod
    def cadastrar_convite(novo_convite: ConviteBase) -> Optional[Convite]:
        convite_novo = novo_convite.model_dump()
        dados_novo_convite = ConviteRepository.create(convite_novo)

        return Convite (**dados_novo_convite)
    

    @staticmethod
    def atualizar_convite(id_convite: int, convite: ConviteBase) -> Optional[Convite]:
        convite_atualizado = convite.model_dump()
        dados_atualizados = ConviteRepository.update(id_convite, convite_atualizado)

        if dados_atualizados is None:
            return None
        
        return Convite(**dados_atualizados)
    

    @staticmethod
    def deletar_convite(id_convite: int) -> bool:
        convite_deletado = ConviteRepository.delete(id_convite)

        return convite_deletado
    