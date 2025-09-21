from app.schemas.jogadores.jogador import JogadorCreate, JogadorResponse, Jogador
from app.database.database import read_database, write_database, delete_jogador

class JogadorService:
    @staticmethod
    def create_jogador(jogador: JogadorCreate) -> JogadorResponse:
        if not jogador.nome or not jogador.idade or not jogador.posicao:
            raise ValueError("Dados do jogador incompletos")
        
        write_database(jogador)

        return JogadorResponse(
            message="Jogador criado com sucesso",
            jogador=jogador
        )
    

    @staticmethod
    def get_all_jogadores() -> list[Jogador]:
        try:
            data = read_database()
            return [Jogador(**j) for j in data.get("jogadores", [])]
        except Exception as e:
            raise ValueError("Erro ao recuperar jogadores: " + str(e))
        

    @staticmethod
    def get_jogador_by_id(jogador_id: int) -> Jogador:
        data = read_database()
        for j in data.get("jogadores", []):
            if j["id"] == jogador_id:
                return Jogador(**j)
        raise ValueError("Jogador não encontrado")
    

    @staticmethod
    def get_jogadores_by_categoria(categoria: str) -> list[Jogador]:
        data = read_database()
        if not categoria:
            raise ValueError("Categoria não fornecida")

        categoria = categoria.strip().lower()
        jogadores_categoria = []
        for j in data.get("jogadores", []):
            if j.get("categoria", "").strip().lower() == categoria:
                jogadores_categoria.append(Jogador(**j))
        return jogadores_categoria
    

    @staticmethod
    def get_jogadores_by_genero(genero: str) -> list[Jogador]:
        data = read_database()
        if not genero:
            raise ValueError("Gênero não fornecido")
        genero = genero.strip().lower()
        jogadores_genero = [
            Jogador(**j) for j in data.get("jogadores", [])
            if j.get("genero", "").strip().lower() == genero
        ]
        return jogadores_genero
    

    @staticmethod
    def get_jogadores_by_categoria_and_genero(categoria: str, genero: str) -> list[Jogador]:
        data = read_database()
        if not categoria or not genero:
            raise ValueError("Categoria ou gênero não fornecidos")
        
        categoria = categoria.strip().lower()
        genero = genero.strip().lower()
        jogadores_filtrados = [
            Jogador(**j) for j in data.get("jogadores", [])
            if j.get("categoria", "").strip().lower() == categoria and
               j.get("genero", "").strip().lower() == genero
        ]
        return jogadores_filtrados
    

    @staticmethod
    def delete_jogador(jogador_id: int) -> None:
        try:
            delete_jogador(jogador_id)
        except Exception as e:
            raise ValueError("Erro ao deletar jogador: " + str(e))
