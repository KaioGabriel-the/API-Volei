import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Dados base para testes
DADOS_NOVA_PARTIDA = {
    "id_criador": 1,
    "id_arena": 1,
    "limite_min": 2,
    "limite_max": 4,
    "idade_min": 10,
    "categoria": "INICIANTE",
    "jogadores": [1, 2]
}

DADOS_ATUALIZACAO = {
    "id_criador": 1,
    "id_arena": 1,
    "limite_min": 3,
    "limite_max": 5,
    "idade_min": 12,
    "categoria": "INICIANTE",
    "jogadores": [1, 2, 3]
}

# Fixture para criar partida antes de testes que precisam de ID existente
@pytest.fixture
def partida_criada():
    response = client.post("/partidas/", json=DADOS_NOVA_PARTIDA)
    assert response.status_code == 201
    return response.json()

# ----------------- Testes -----------------

def test_criar_partida_sucesso():
    response = client.post("/partidas/", json=DADOS_NOVA_PARTIDA)
    assert response.status_code == 201
    data = response.json()
    assert data["id_criador"] == DADOS_NOVA_PARTIDA["id_criador"]
    assert data["id_arena"] == DADOS_NOVA_PARTIDA["id_arena"]

def test_buscar_partida_por_id_sucesso(partida_criada):
    id_partida = partida_criada["id_partida"]
    response = client.get(f"/partidas/partida/{id_partida}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_partida"] == id_partida

def test_atualizar_partida_sucesso(partida_criada):
    id_partida = partida_criada["id_partida"]
    response = client.put(f"/partidas/{id_partida}", json=DADOS_ATUALIZACAO)
    assert response.status_code == 200
    data = response.json()
    assert data["limite_min"] == DADOS_ATUALIZACAO["limite_min"]
    assert data["limite_max"] == DADOS_ATUALIZACAO["limite_max"]

def test_deletar_partida_sucesso(partida_criada):
    id_partida = partida_criada["id_partida"]
    response = client.delete(f"/partidas/{id_partida}")
    assert response.status_code == 204
    # Confirma que não existe mais
    response = client.get(f"/partidas/partida/{id_partida}")
    assert response.status_code == 404

def test_criar_partida_limite_invalido():
    dados_invalidos = DADOS_NOVA_PARTIDA.copy()
    dados_invalidos["limite_max"] = 1
    dados_invalidos["limite_min"] = 3
    response = client.post("/partidas/", json=dados_invalidos)
    assert response.status_code == 422

def test_criar_partida_idade_negativa():
    dados_invalidos = DADOS_NOVA_PARTIDA.copy()
    dados_invalidos["idade_min"] = -5
    response = client.post("/partidas/", json=dados_invalidos)
    assert response.status_code == 422

def test_criar_partida_jogadores_duplicados():
    dados_invalidos = DADOS_NOVA_PARTIDA.copy()
    dados_invalidos["jogadores"] = [1, 2, 2]
    response = client.post("/partidas/", json=dados_invalidos)
    assert response.status_code == 422
