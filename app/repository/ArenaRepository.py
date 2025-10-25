from app.db import arenas
from typing import List, Dict, Optional, Any

def _get_next_id() -> int:
    dados = arenas.DADOS_ARENAS
    if not dados:
        return 1
    
    return max(item["id"] for item in dados) + 1


class ArenaRepository:
    @staticmethod
    def get_all() -> List[Dict]:
        return arenas.DADOS_ARENAS.copy()
    

    @staticmethod
    def get_by_id(id_arena) -> Optional [Dict]:
        dados = arenas.DADOS_ARENAS.copy()
        arena = next((item  for item in dados if item["id"] == id_arena), None)

        return arena
    

    @staticmethod
    def create(arena_nova: Dict[str, any]) -> Optional[Dict]:
        novo_id = _get_next_id()
        nova_arena = arena_nova.copy()
        nova_arena["id"] = novo_id
        arenas.DADOS_ARENAS.append(nova_arena)
        return nova_arena


    @staticmethod
    def delete(id_arena: int) -> bool:
        dados = arenas.DADOS_ARENAS

        try:
            index_to_delete = next((i for i, item in enumerate(dados) if item["id"] == id_arena))
            dados.pop(index_to_delete)
            
            return True 
        except StopIteration:
            return False
        
    
    @staticmethod
    def update(id_arena: int, arena_data: Dict[str, Any]) -> Optional[Dict]:
        dados = arenas.DADOS_ARENAS
        
        try:
            index_to_update = next((i for i, item in enumerate(dados) if item["id"] == id_arena))
            
            arena_atualizado = arena_data.copy()
            arena_atualizado["id"] = id_arena

            dados[index_to_update] = arena_atualizado
            
            return arena_atualizado
            
        except StopIteration:
            return None
        