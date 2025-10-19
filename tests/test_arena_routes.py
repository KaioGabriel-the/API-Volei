from fastapi.testclient import TestClient
from fastapi import status, HTTPException # Adicionando HTTPException para o teste de cadastro
from main import app 
import pytest
from unittest.mock import patch, AsyncMock

# Configuração do TestClient
client = TestClient(app)

# --- DADOS DE TESTE REUTILIZÁVEIS ---

# Mantendo os dados de mock completos para que a validação de entrada (se houver) e o handler funcionem.
# No entanto, a aplicação FastAPI, devido a um schema que omite 'cidade' e 'capacidade',
# irá remover esses campos na resposta final.
MOCK_ARENA_DATA = [
    {
        "id": 1,
        "nome": "Maracanã",
        "cidade": "Rio de Janeiro",
        "capacidade": 78838,
        "enderecao": "Rua Professor Eurico Rabelo, Maracanã",
        "valor_hora": 250.00,
        "qtd_jogadores": 12
    },
    {
        "id": 2,
        "nome": "Allianz Parque",
        "cidade": "São Paulo",
        "capacidade": 43765,
        "enderecao": "Av. Francisco Matarazzo, Água Branca",
        "valor_hora": 300.50,
        "qtd_jogadores": 10
    },
]

# Dados para teste de cadastro e atualização (no formato ArenaBase)
NOVA_ARENA_DATA = {
    "nome": "Ginásio Ibirapuera",
    "enderecao": "Rua Ibirapuera, 100",
    "valor_hora": 150.00,
    "qtd_jogadores": 10
}


# --- PATHS PARA MOCKING (CORRIGIDO) ---
# Define os paths de mocking para as funções do handler:

# 1. Path para o handler de listagem (GET /arenas)
LISTAR_HANDLER_PATH = "app.handlers.ArenaHandler.ArenaHandler.listar"

# 2. Path para o handler de busca por ID (GET /arenas/{id})
BUSCAR_HANDLER_PATH = "app.handlers.ArenaHandler.ArenaHandler.buscar" 

# NOVOS PATHS ADICIONADOS:

# 3. Path para o handler de cadastro (POST /arenas)
CADASTRAR_HANDLER_PATH = "app.handlers.ArenaHandler.ArenaHandler.cadastrar"

# 4. Path para o handler de atualização (PUT /arenas/{id})
ATUALIZAR_HANDLER_PATH = "app.handlers.ArenaHandler.ArenaHandler.atualizar"

# 5. Path para o handler de deleção (DELETE /arenas/{id})
DELETAR_HANDLER_PATH = "app.handlers.ArenaHandler.ArenaHandler.deletar"


# --- TESTES DE LEITURA (GET /arenas) ---

def test_listar_arenas_sucesso():
    """Testa se a listagem de arenas retorna o status 200 e os dados esperados."""
    
    # Mocka a chamada assíncrona de listar para retornar dados mockados
    with patch(LISTAR_HANDLER_PATH, new_callable=AsyncMock) as mock_listar:
        mock_listar.return_value = MOCK_ARENA_DATA
        
        response = client.get("/arenas") # Assumindo que o prefixo é /arenas
        
        assert response.status_code == 200
        data = response.json()
        
        # Verifica se o handler foi chamado
        mock_listar.assert_called_once()
        
        # Verifica se a resposta contém a lista de dados mockados
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["nome"] == "Maracanã"


def test_listar_arenas_vazia_retorno_none():
    """
    Testa o caso específico onde ArenaHandler.listar() retorna None,
    o que a rota deve converter para uma lista vazia ([]).
    """
    with patch(LISTAR_HANDLER_PATH, new_callable=AsyncMock) as mock_listar:
        # Simula o retorno None do handler
        mock_listar.return_value = None 
        
        response = client.get("/arenas")
        
        assert response.status_code == 200
        data = response.json()
        
        mock_listar.assert_called_once()
        
        # O retorno esperado é uma lista vazia, conforme a lógica da rota
        assert data == []

def test_listar_arenas_vazia_retorno_lista_vazia():
    """Testa o caso padrão onde ArenaHandler.listar() retorna uma lista vazia."""
    with patch(LISTAR_HANDLER_PATH, new_callable=AsyncMock) as mock_listar:
        # Simula o retorno de uma lista vazia
        mock_listar.return_value = []
        
        response = client.get("/arenas")
        
        assert response.status_code == 200
        data = response.json()
        
        mock_listar.assert_called_once()
        
        # O retorno esperado é uma lista vazia
        assert data == []
        
def test_listar_arenas_dados_estruturados():
    """Testa a estrutura mínima de um item retornado."""
    with patch(LISTAR_HANDLER_PATH, new_callable=AsyncMock) as mock_listar:
        mock_listar.return_value = MOCK_ARENA_DATA
        
        response = client.get("/arenas")
        data = response.json()
        
        assert response.status_code == 200
        assert len(data) > 0 # Garantir que há dados para checar
        
        # Verifica a estrutura do primeiro item
        primeira_arena = data[0]
        assert "id" in primeira_arena
        assert isinstance(primeira_arena["id"], int)
        assert "nome" in primeira_arena
        assert isinstance(primeira_arena["nome"], str)
        assert isinstance(primeira_arena["enderecao"], str)
        assert "valor_hora" in primeira_arena
        # Assumindo que valor_hora pode ser float
        assert isinstance(primeira_arena["valor_hora"], (float, int))
        assert "qtd_jogadores" in primeira_arena
        assert isinstance(primeira_arena["qtd_jogadores"], int)


# --- TESTES DE BUSCA (GET /{id_arena}) ---

def test_buscar_arena_por_id_sucesso():
    """Testa a busca de uma arena por ID com sucesso."""
    arena_esperada = MOCK_ARENA_DATA[0]
    id_arena = arena_esperada["id"]

    # CORREÇÃO APLICADA: Usando BUSCAR_HANDLER_PATH corrigido
    with patch(BUSCAR_HANDLER_PATH, new_callable=AsyncMock) as mock_buscar:
        # O handler retorna a arena completa
        mock_buscar.return_value = arena_esperada

        response = client.get(f"/arenas/{id_arena}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Agora, esta linha deve passar, pois o mock está aplicado à função correta
        mock_buscar.assert_called_once()
        assert data["id"] == id_arena
        assert data["nome"] == arena_esperada["nome"]
        # ... outras assertions


def test_buscar_arena_por_id_nao_encontrada():
    """Testa se a rota retorna 404 quando a arena não é encontrada."""
    id_arena = 999 # ID que não existe

    # CORREÇÃO APLICADA: Usando BUSCAR_HANDLER_PATH corrigido
    with patch(BUSCAR_HANDLER_PATH, new_callable=AsyncMock) as mock_buscar:
        # O handler retorna None, acionando a HTTPException na rota
        mock_buscar.return_value = None

        response = client.get(f"/arenas/{id_arena}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()

        # Agora, esta linha deve passar
        mock_buscar.assert_called_once()
        # CORREÇÃO: Atualizando a mensagem esperada para corresponder à mensagem da rota
        assert data["detail"] == f"Arena com id {id_arena} não encontrada."


def test_buscar_arena_por_id_dados_estruturados():
    """Testa a estrutura mínima do item retornado pela busca por ID."""
    arena_esperada = MOCK_ARENA_DATA[1]
    id_arena = arena_esperada["id"]

    # CORREÇÃO APLICADA: Usando BUSCAR_HANDLER_PATH corrigido
    with patch(BUSCAR_HANDLER_PATH, new_callable=AsyncMock) as mock_buscar:
        mock_buscar.return_value = arena_esperada
        
        response = client.get(f"/arenas/{id_arena}")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        mock_buscar.assert_called_once()
        
        # Verifica a estrutura mínima da resposta
        assert "id" in data
        assert isinstance(data["id"], int)
        assert "nome" in data
        assert isinstance(data["nome"], str)
        assert "enderecao" in data
        assert isinstance(data["enderecao"], str)
        assert "valor_hora" in data
        assert isinstance(data["valor_hora"], (float, int))
        assert "qtd_jogadores" in data
        assert isinstance(data["qtd_jogadores"], int)


# --- NOVOS TESTES: CRIAÇÃO (POST /arenas) ---

def test_cadastrar_arena_sucesso():
    """Testa o cadastro de uma nova arena com sucesso (201 Created)."""
    # Usamos o primeiro item mockado como o resultado esperado
    arena_criada = MOCK_ARENA_DATA[0] 
    
    with patch(CADASTRAR_HANDLER_PATH, new_callable=AsyncMock) as mock_cadastrar:
        mock_cadastrar.return_value = arena_criada
        
        response = client.post("/arenas", json=NOVA_ARENA_DATA)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Verifica se o handler foi chamado
        mock_cadastrar.assert_called_once()
        
        # FIX: Pydantic converte o JSON em uma instância de modelo (ArenaBase) antes de chamar o handler.
        # Precisamos verificar os atributos da instância passada, e não o dicionário original.
        called_arg = mock_cadastrar.call_args[0][0]
        
        assert called_arg.nome == NOVA_ARENA_DATA["nome"]
        assert called_arg.enderecao == NOVA_ARENA_DATA["enderecao"]
        assert called_arg.valor_hora == NOVA_ARENA_DATA["valor_hora"]
        assert called_arg.qtd_jogadores == NOVA_ARENA_DATA["qtd_jogadores"]

        assert data["nome"] == arena_criada["nome"]
        assert "id" in data # Verifica se o ID foi retornado

def test_cadastrar_arena_dados_incompletos_handler_fail():
    """Testa se a rota retorna 422 quando o handler sinaliza falha nos dados (simulando HTTPException)."""
    
    with patch(CADASTRAR_HANDLER_PATH, new_callable=AsyncMock) as mock_cadastrar:
        # Simula o retorno que aciona a verificação `if dados_arena is HTTPException:` na rota
        mock_cadastrar.return_value = HTTPException 
        
        # Faz a requisição com dados válidos, mas o mock simula a falha de processamento no handler
        response = client.post("/arenas", json=NOVA_ARENA_DATA)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"] == "Dados incompletos da arena. Não foi possível realizar o cadastrato."
        mock_cadastrar.assert_called_once()


# --- NOVOS TESTES: ATUALIZAÇÃO (PUT /arenas/{id}) ---

DADOS_ATUALIZACAO = {
    "nome": "Novo Nome Arena",
    "enderecao": "Nova Rua, 100",
    "valor_hora": 100.00,
    "qtd_jogadores": 8
}

def test_atualizar_arena_sucesso():
    """Testa a atualização de uma arena existente com sucesso (200 OK)."""
    id_arena = 1
    # Simula o objeto de arena que seria retornado pelo handler após a atualização
    arena_atualizada = MOCK_ARENA_DATA[0].copy()
    arena_atualizada.update(DADOS_ATUALIZACAO)
    
    with patch(ATUALIZAR_HANDLER_PATH, new_callable=AsyncMock) as mock_atualizar:
        mock_atualizar.return_value = arena_atualizada
        
        response = client.put(f"/arenas/{id_arena}", json=DADOS_ATUALIZACAO)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verifica se o handler foi chamado com os parâmetros corretos
        mock_atualizar.assert_called_once()
        
        # FIX: Pydantic converte o JSON em uma instância de modelo (ArenaBase)
        # Verificamos que o ID foi passado corretamente e os atributos do objeto ArenaBase.
        called_args = mock_atualizar.call_args[0]
        called_id = called_args[0]
        called_arena_data = called_args[1]
        
        assert called_id == id_arena
        assert called_arena_data.nome == DADOS_ATUALIZACAO["nome"]
        assert called_arena_data.qtd_jogadores == DADOS_ATUALIZACAO["qtd_jogadores"]
        
        assert data["id"] == id_arena
        assert data["nome"] == DADOS_ATUALIZACAO["nome"]
        assert data["qtd_jogadores"] == DADOS_ATUALIZACAO["qtd_jogadores"]

def test_atualizar_arena_nao_encontrada():
    """Testa se a rota retorna 404 ao tentar atualizar uma arena inexistente."""
    id_arena = 999
    
    with patch(ATUALIZAR_HANDLER_PATH, new_callable=AsyncMock) as mock_atualizar:
        mock_atualizar.return_value = None # Handler retorna None se não encontrar
        
        response = client.put(f"/arenas/{id_arena}", json=DADOS_ATUALIZACAO)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        
        mock_atualizar.assert_called_once()
        assert data["detail"] == f"Arena com id {id_arena} não encontrada para atualização."


# --- NOVOS TESTES: DELEÇÃO (DELETE /arenas/{id}) ---

def test_deletar_arena_sucesso():
    """Testa a deleção de uma arena existente com sucesso (204 No Content)."""
    id_arena = 1
    
    with patch(DELETAR_HANDLER_PATH, new_callable=AsyncMock) as mock_deletar:
        mock_deletar.return_value = True # Handler retorna True em caso de sucesso
        
        response = client.delete(f"/arenas/{id_arena}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.content # 204 deve retornar corpo vazio
        
        mock_deletar.assert_called_once_with(id_arena)

def test_deletar_arena_nao_encontrada():
    """Testa se a rota retorna 404 ao tentar deletar uma arena inexistente."""
    id_arena = 999
    
    with patch(DELETAR_HANDLER_PATH, new_callable=AsyncMock) as mock_deletar:
        mock_deletar.return_value = False # Handler retorna False se não encontrar
        
        response = client.delete(f"/arenas/{id_arena}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        
        mock_deletar.assert_called_once_with(id_arena)
        assert data["detail"] == f"Arena com id {id_arena} não encontrada para exclusão."
