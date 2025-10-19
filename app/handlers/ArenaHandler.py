from app.schemas.Arena import Arena, ArenaBase
from app.services.ArenaService import ArenaService
from typing import List, Optional

class ArenaHandler:

    @staticmethod
    async def listar() -> Optional[List[Arena]]:
        list_arena = ArenaService.listar_arenas()

        return list_arena
    

    @staticmethod
    async def buscar(id_arena: int) -> Optional[Arena]:
        arena = ArenaService.buscar_arena(id_arena)
        
        return arena
    

    @staticmethod
    async def cadastrar(nova_arena: ArenaBase) -> Optional[Arena]:
        arena = ArenaService.cadastrar_arena(nova_arena)

        return arena
    

    @staticmethod
    async def deletar(id_arena: int) -> bool:
        deletado = ArenaService.deletar_arena(id_arena)
        return deletado
    

    @staticmethod
    async def atualizar(id_arena:int, arena_data:ArenaBase) -> Optional[Arena]:
        arena_atualizado = ArenaService.atualizar_arena(id_arena, arena_data)
        return arena_atualizado