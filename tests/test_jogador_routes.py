from fastapi.testclient import TestClient
from main import app 
from app.db.jogadores import DADOS_JOGADORES
from app.enums.jogador.Posicao import Poiscao
import pytest 
import copy # Importar copy para garantir que a cópia inicial seja profunda se necessário, embora DADOS_JOGADORES seja uma lista de dicionários simples aqui.

# Configuração do TestClient
client = TestClient(app)

# --- FIXTURE PARA LIMPEZA DE DADOS ---
@pytest.fixture(autouse=True)
def cleanup_data():
    """
    Fixture que garante que os DADOS_JOGADORES sejam restaurados
    ao seu estado inicial após a execução de cada teste.
    """
    # Usar copy.deepcopy() se a estrutura de dados fosse mais complexa,
    # mas copy.copy() ou [:], junto com o fato de serem dicts simples,
    # já é suficiente para restaurar o estado da lista.
    initial_data = copy.copy(DADOS_JOGADORES) 
    
    yield 
    
    # Restaura o estado da lista DADOS_JOGADORES após o teste
    DADOS_JOGADORES.clear()
    DADOS_JOGADORES.extend(initial_data)

# --- DADOS DE TESTE REUTILIZÁVEIS ---

DADOS_ATUALIZACAO = {
    "nome": "Leila Pires",
    "idade": 50,
    "genero": "FEMININO",
    "posicao": "PONTEIRO",
    "nivel": "EXPERIENTE"
}

DADOS_NOVO_JOGADOR = {
    "nome": "Leila Barros",
    "idade": 49,
    "genero": "FEMININO",
    "posicao": "OPOSTO",
    "nivel": "EXPERIENTE"
}

# --- TESTES DE LEITURA (GET) ---

def test_listar_jogadores_status_code():
    """Testa se a listagem de jogadores retorna o status 200."""
    response = client.get("/jogadores")
    assert response.status_code == 200

def test_listar_jogadores_dados():
    """Testa se a listagem retorna uma lista com os campos esperados."""
    response = client.get("/jogadores/")
    data = response.json()
    assert isinstance(data, list)
    # Verifica a estrutura do primeiro jogador (se a lista não estiver vazia)
    if data:
        primeiro_jogador = data[0]
        assert "id" in primeiro_jogador
        assert "nome" in primeiro_jogador
        assert "idade" in primeiro_jogador
        assert "posicao" in primeiro_jogador
        assert "genero" in primeiro_jogador
        assert "nivel" in primeiro_jogador

def test_buscar_jogador_por_id_sucesso():
    """Testa a busca de um jogador existente por ID."""
    # Assumindo que o ID 1 sempre existe no DADOS_JOGADORES inicial
    id_valido = 1
    response = client.get(f"/jogadores/{id_valido}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == id_valido
    assert "nome" in data
    assert "idade" in data
    assert "posicao" in data
    assert "genero" in data
    assert "nivel" in data

def test_buscar_jogador_por_id_nao_encontrado():
    """Testa a busca por um ID que não existe."""
    id_invalido = 999
    response = client.get(f"/jogadores/{id_invalido}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == f"Jogador com id {id_invalido} não encontrado."


# --- TESTES DE CRIAÇÃO (POST) ---

def test_criar_jogador_sucesso():
    """Testa a criação de um novo jogador com dados válidos."""
    response = client.post("/jogadores/", json=DADOS_NOVO_JOGADOR)
    
    assert response.status_code == 201
    
    data = response.json()
    
    # Verifica se o ID foi gerado e é um inteiro
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["nome"] == DADOS_NOVO_JOGADOR["nome"]
    
    # Verifica se o jogador foi realmente adicionado à lista interna
    jogador_interno = next((item for item in DADOS_JOGADORES if item["id"] == data["id"]), None)
    assert jogador_interno is not None


def test_criar_jogador_falha_validacao_campos_ausentes():
    """Testa a falha de validação quando campos obrigatórios estão ausentes."""
    dados_invalidos = {
        "nome": "Zeca",
        "idade": 25,
        # Faltando 'genero', 'posicao', 'nivel'
    }
    
    response = client.post("/jogadores/", json=dados_invalidos)
    
    assert response.status_code == 422
    
    data = response.json()
    
    assert "detail" in data
    
    # Verifica se a mensagem de erro para um campo obrigatório ausente está presente
    erro_genero = next((err for err in data["detail"] if err["loc"] == ["body", "genero"]), None)
    assert erro_genero is not None
    # Verifica se a mensagem de campo obrigatório está presente (pode variar ligeiramente)
    assert "Field required" in erro_genero["msg"] or "field required" in erro_genero["msg"] 


# --- TESTES DE ATUALIZAÇÃO (PUT) ---

def test_atualizar_jogador_sucesso():
    """Testa a atualização bem-sucedida de um jogador existente."""
    id_a_atualizar = 1 
    
    response = client.put(f"/jogadores/{id_a_atualizar}", json=DADOS_ATUALIZACAO)
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Verifica os dados retornados na resposta
    assert data["id"] == id_a_atualizar
    assert data["nome"] == "Leila Pires"
    assert data["posicao"] == "PONTEIRO" 
    
    # Verifica se a lista interna foi realmente atualizada
    jogador_interno = next((item for item in DADOS_JOGADORES if item["id"] == id_a_atualizar), None)
    assert jogador_interno is not None
    assert jogador_interno["posicao"] == Poiscao.PONTEIRO
    

def test_atualizar_jogador_nao_encontrado():
    """Testa a tentativa de atualizar um jogador com ID inexistente."""
    id_inexistente = 999 
    tamanho_antes = len(DADOS_JOGADORES)
    
    response = client.put(f"/jogadores/{id_inexistente}", json=DADOS_ATUALIZACAO)
    
    assert response.status_code == 404
    
    data = response.json()
    
    assert "detail" in data
    assert f"Jogador com id {id_inexistente} não encontrado para atualização." in data["detail"]
    
    # Verifica se o tamanho da lista não mudou
    assert len(DADOS_JOGADORES) == tamanho_antes
    
    
def test_atualizar_jogador_falha_validacao_tipo():
    """Testa a falha de validação com tipo de dado incorreto (idade como string)."""
    id_a_atualizar = 1
    dados_invalidos = DADOS_ATUALIZACAO.copy()
    dados_invalidos["idade"] = "cinquenta" # Tipo incorreto (string em vez de int)

    response = client.put(f"/jogadores/{id_a_atualizar}", json=dados_invalidos)
    
    assert response.status_code == 422
    
    data = response.json()
    
    assert "detail" in data
    
    # Verifica se a mensagem de erro de tipo de dado incorreto está presente
    erro_idade = next((err for err in data["detail"] if err["loc"] == ["body", "idade"]), None)
    assert erro_idade is not None
    # A mensagem pode variar (pydantic/fastapi), mas deve indicar erro de tipo
    assert "Input should be a valid integer" in erro_idade["msg"] or "valid integer" in erro_idade["msg"]


# --- TESTES DE EXCLUSÃO (DELETE) ---

def test_deletar_jogador_sucesso():
    """Testa a exclusão bem-sucedida de um jogador existente."""
    id_a_deletar = 1 
    
    tamanho_antes = len(DADOS_JOGADORES)
    
    response = client.delete(f"/jogadores/{id_a_deletar}")
    
    assert response.status_code == 204 # Status Code 204 significa 'No Content' (Sucesso sem corpo)
    
    assert response.text == "" # O corpo deve ser vazio (No Content)
    
    # Verifica se a lista interna foi reduzida
    assert len(DADOS_JOGADORES) == tamanho_antes - 1
    
    # Verifica se o jogador foi removido da lista interna
    jogador_removido = next((item for item in DADOS_JOGADORES if item["id"] == id_a_deletar), None)
    assert jogador_removido is None


def test_deletar_jogador_nao_encontrado():
    """Testa a tentativa de excluir um jogador com ID inexistente."""
    id_inexistente = 999 
    
    tamanho_antes = len(DADOS_JOGADORES)
    
    response = client.delete(f"/jogadores/{id_inexistente}")
    
    assert response.status_code == 404
    
    data = response.json()
    
    assert "detail" in data
    assert data["detail"] == f"Jogador com id {id_inexistente} não encontrado para exclusão."
    
    # Verifica se o tamanho da lista não mudou
    assert len(DADOS_JOGADORES) == tamanho_antes
