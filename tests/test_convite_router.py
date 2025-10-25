from fastapi.testclient import TestClient
from main import app
import pytest
import copy

# Supondo que exista algo como DADOS_CONVITES sendo usado pelo ConviteHandler
from app.db.convites import DADOS_CONVITES  

client = TestClient(app)

# --- FIXTURE PARA LIMPEZA DE DADOS ---

@pytest.fixture(autouse=True)
def cleanup_data():
    """Restaura os convites após cada teste."""
    initial_data = copy.deepcopy(DADOS_CONVITES)
    yield
    DADOS_CONVITES.clear()
    DADOS_CONVITES.extend(initial_data)


# --- DADOS DE TESTE ---

DADOS_NOVO_CONVITE = {
    "id_remetente": 1,
    "id_partida": 10,
    "status": "Pendente"
}

DADOS_ATUALIZACAO = {
    "id_remetente": 1,
    "id_partida": 10,
    "status": "Aceito"
}


# --- TESTES DE LEITURA (GET) ---

def test_listar_convites_status_code():
    """Testa se a listagem de convites retorna status 200."""
    response = client.get("/convites/")
    assert response.status_code == 200


def test_listar_convites_dados():
    """Testa se a listagem retorna uma lista com os campos esperados."""
    response = client.get("/convites/")
    data = response.json()
    assert isinstance(data, list)
    if data:
        convite = data[0]
        assert "id_convite" in convite
        assert "id_remetente" in convite
        assert "id_partida" in convite
        assert "status" in convite


def test_buscar_convite_por_id_sucesso():
    """Testa a busca de um convite existente por ID."""
    id_valido = 1
    response = client.get(f"/convites/convite/{id_valido}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_convite"] == id_valido
    assert "status" in data


def test_buscar_convite_por_id_nao_encontrado():
    """Testa busca de convite inexistente."""
    id_invalido = 999
    response = client.get(f"/convites/convite/{id_invalido}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Convite com id {id_invalido} não encontrado."


def test_buscar_convites_por_remetente():
    """Testa a listagem de convites por remetente."""
    id_remetente = 1
    response = client.get(f"/convites/remetente/{id_remetente}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for c in data:
        assert c["id_remetente"] == id_remetente


# --- TESTES DE CRIAÇÃO (POST) ---

def test_criar_convite_sucesso():
    """Testa a criação de um novo convite válido."""
    response = client.post("/convites/", json=DADOS_NOVO_CONVITE)
    assert response.status_code == 201
    data = response.json()
    assert "id_convite" in data
    assert data["status"] == "Pendente"

    # Verifica se foi realmente salvo
    convite_interno = next((c for c in DADOS_CONVITES if c["id_convite"] == data["id_convite"]), None)
    assert convite_interno is not None


def test_criar_convite_campos_incompletos():
    """Testa erro ao criar convite com campos ausentes."""
    dados_invalidos = {"id_remetente": 1}
    response = client.post("/convites/", json=dados_invalidos)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


# --- TESTES DE ATUALIZAÇÃO (PUT) ---

def test_atualizar_convite_sucesso():
    """Testa atualização de convite existente."""
    id_convite = 1
    response = client.put(f"/convites/{id_convite}", json=DADOS_ATUALIZACAO)
    assert response.status_code == 200
    data = response.json()
    assert data["id_convite"] == id_convite
    assert data["status"] == "Aceito"


def test_atualizar_convite_nao_encontrado():
    """Testa atualização de convite inexistente."""
    id_invalido = 999
    response = client.put(f"/convites/{id_invalido}", json=DADOS_ATUALIZACAO)
    assert response.status_code == 404
    data = response.json()
    assert f"Convite com id {id_invalido} não encontrado" in data["detail"]


def test_atualizar_convite_tipo_incorreto():
    """Testa erro ao atualizar convite com tipo incorreto."""
    id_convite = 1
    dados_invalidos = DADOS_ATUALIZACAO.copy()
    dados_invalidos["id_partida"] = "dez"  # deveria ser int
    response = client.put(f"/convites/{id_convite}", json=dados_invalidos)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


# --- TESTES DE EXCLUSÃO (DELETE) ---

def test_deletar_convite_sucesso():
    """Testa exclusão bem-sucedida de um convite existente."""
    id_convite = 1
    tamanho_antes = len(DADOS_CONVITES)
    response = client.delete(f"/convites/{id_convite}")
    assert response.status_code == 204
    assert len(DADOS_CONVITES) == tamanho_antes - 1


def test_deletar_convite_nao_encontrado():
    """Testa tentativa de excluir convite inexistente."""
    id_invalido = 999
    tamanho_antes = len(DADOS_CONVITES)
    response = client.delete(f"/convites/{id_invalido}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Convite com id {id_invalido} não encontrado para exclusão."
    assert len(DADOS_CONVITES) == tamanho_antes
