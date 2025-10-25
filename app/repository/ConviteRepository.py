from typing import List, Dict, Optional
from app.db import convites


def _get_next_id() -> int:
    dados = convites.DADOS_CONVITES
    if not dados:
        return 1
    
    return max(item["id_convite"] for item in dados) + 1


class ConviteRepository:
    @staticmethod
    def get_all() -> List[Dict]:
        dados = convites.DADOS_CONVITES.copy()

        return dados
    

    @staticmethod
    def get_by_id(id_convite: int) -> Dict:
        dados = convites.DADOS_CONVITES.copy()
        dado = next((item for item in dados if item["id_convite"] == id_convite), None)

        return dado
    

    @staticmethod
    def get_by_id_remetente(id_remetente: int) -> List[Dict]:
        dados = convites.DADOS_CONVITES.copy()
        dados_remetente = [item for item in dados if item["id_remetente"] == id_remetente]

        return dados_remetente
    

    @staticmethod
    def create(novo_convite: Dict[str, any]) -> Optional[Dict]:
        novo_id = _get_next_id()
        convite_novo = novo_convite.copy()
        convite_novo["id_convite"] = novo_id
        convites.DADOS_CONVITES.append(convite_novo)
        return convite_novo
    

    @staticmethod
    def update(id_convite: int, convite: Dict) -> Dict:
        dados = convites.DADOS_CONVITES.copy()

        try:
            index_to_update = next((i for i, item in enumerate(dados) if item["id_convite"] == id_convite))
            convite_atualizado = convite.copy()
            convite_atualizado["id_convite"] = id_convite
            dados[index_to_update] = convite_atualizado

            return convite_atualizado
        except StopIteration:
            None

    
    @staticmethod
    def delete(id_convite: int) -> bool:
        dados = convites.DADOS_CONVITES

        try:
            index_to_update = next((i for i, item in enumerate(dados) if item["id_convite"] == id_convite))
            dados.pop(index_to_update)
            return True
        except StopIteration:
            False
            