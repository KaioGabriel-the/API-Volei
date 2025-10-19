from app.schemas.Arena import Arena, ArenaBase
from app.repository.ArenaRepository import ArenaRepository
from typing import List, Optional

class ArenaService:

    @staticmethod
    def listar_arenas() -> Optional[List[Arena]]:
        dados_arena = ArenaRepository.get_all()

        arenas_formatadas = [Arena(**i) for i in dados_arena]

        return arenas_formatadas
    

    @staticmethod
    def buscar_arena(id_arena: int) -> Optional[Arena]:
        dados_arena = ArenaRepository.get_by_id(id_arena)

        if dados_arena is None:
            return None
        
        return Arena(**dados_arena)
    

    @staticmethod
    def cadastrar_arena(nova_arena: ArenaBase) -> Optional[Arena]:
        arena_nova = nova_arena.model_dump()
        arena = ArenaRepository.create(arena_nova)

        return Arena(**arena)
    

    @staticmethod
    def deletar_arena(id_arena: int) -> bool:
        deletado = ArenaRepository.delete(id_arena)
        return deletado
    

    @staticmethod
    def atualizar_arena(id_arena: int, arena_data: ArenaBase) -> Optional[Arena]:
        data_dict = arena_data.model_dump()
        
        arena_atualizado_dict = ArenaRepository.update(id_arena, data_dict)
        
        if arena_atualizado_dict is None:
            return None 
        
        return Arena(**arena_atualizado_dict)