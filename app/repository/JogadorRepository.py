from app.db import jogadores
from typing import List, Optional, Dict, Any

def _get_next_id() -> int:
    dados = jogadores.DADOS_JOGADORES
    if not dados:
        return 1
    
    return max(item["id"] for item in dados) + 1


class JogadorRepository():
    def get_all() -> List[dict]:
        return jogadores.DADOS_JOGADORES.copy()
    

    def get_by_id(id_jogador: int) -> Optional [dict]:
        dados = jogadores.DADOS_JOGADORES.copy()
        jogador = next((item  for item in dados if item["id"] == id_jogador), None)

        return jogador
    

    def create(jogador_data: Dict[str, Any])  -> Dict:
        novo_id = _get_next_id()
        novo_jogador = jogador_data.copy()
        novo_jogador["id"] = novo_id
        jogadores.DADOS_JOGADORES.append(novo_jogador)
        return novo_jogador
    

    @staticmethod
    def delete(id_jogador: int) -> bool:
        dados = jogadores.DADOS_JOGADORES
        
        try:
            index_to_delete = next(
                (i for i, item in enumerate(dados) if item["id"] == id_jogador)
            )
            
            dados.pop(index_to_delete)
            
            return True 
            
        except StopIteration:
            return False 
        

    @staticmethod
    def update(id_jogador: int, jogador_data: Dict[str, Any]) -> Optional[Dict]:
        dados = jogadores.DADOS_JOGADORES
        
        try:
            index_to_update = next(
                (i for i, item in enumerate(dados) if item["id"] == id_jogador)
            )
            
            jogador_atualizado = jogador_data.copy()
            jogador_atualizado["id"] = id_jogador 

            dados[index_to_update] = jogador_atualizado
            
            return jogador_atualizado
            
        except StopIteration:
            return None
