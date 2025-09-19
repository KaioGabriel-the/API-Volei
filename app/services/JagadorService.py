from schemas.jogadores.jogador import JogadorCreate, JogadorResponse

class JogadorService:
    @staticmethod
    def create_jogador(jogador: JogadorCreate) -> JogadorResponse:
        if not jogador.nome or not jogador.idade or not jogador.posicao:
            raise ValueError("Dados do jogador incompletos")
        return JogadorResponse(
            message="Jogador criado com sucesso",
            jogador=jogador  # aqui incluímos o objeto jogador
        )
