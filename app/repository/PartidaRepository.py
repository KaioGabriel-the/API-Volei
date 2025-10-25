from app.db import partidas
from typing import List, Dict, Optional, Any


def _get_next_id() -> int:
    dados = partidas.DADOS_PARTIDAS
    if not dados:
        return 1
    
    return max(item["id_partida"] for item in dados) + 1


class PartidaRepository:
    @staticmethod
    def get_all() -> List[Dict]:
        dados = partidas.DADOS_PARTIDAS.copy()

        return dados
    

    @staticmethod
    def get_by_id(id_partida: int) -> Dict:
        dados = partidas.DADOS_PARTIDAS.copy()
        dado = next((item for item in dados if item["id_partida"] == id_partida), None)

        return dado
    

    @staticmethod
    def get_by_id_jogador(id_jogador: int) -> List[Dict]:
        dados = partidas.DADOS_PARTIDAS.copy()
        dados_partidas = [item for item in dados if item["id_criador"] == id_jogador]

        return dados_partidas
    

    @staticmethod
    def create(nova_parida: Dict[str, any]) -> Optional[Dict]:
        novo_id = _get_next_id()
        partida_nova = nova_parida.copy()
        partida_nova["id_partida"] = novo_id
        partidas.DADOS_PARTIDAS.append(partida_nova)
        return partida_nova
    

    @staticmethod
    def update(id_partida: int, partida: Dict) -> Dict:
        dados = partidas.DADOS_PARTIDAS.copy()

        try:
            index_to_update = next((i for i, item in enumerate(dados) if item["id_partida"] == id_partida))
            partida_atualizada = partida.copy()
            partida_atualizada["id_partida"] = id_partida
            dados[index_to_update] = partida_atualizada

            return partida_atualizada
        except StopIteration:
            None

    
    @staticmethod
    def delete(id_partida: int) -> bool:
        dados = partidas.DADOS_PARTIDAS

        try:
            index_to_update = next((i for i, item in enumerate(dados) if item["id_partida"] == id_partida))
            dados.pop(index_to_update)
            return True
        except StopIteration:
            False