from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_jogadores_status_code():
    response = client.get("/jogadores")
    assert response.status_code == 200


def test_listar_jogadores_dados():
    response = client.get("/jogadores/")
    data = response.json()
    assert isinstance(data, list)
    primeiro_jogador = data[0]
    assert "id" in primeiro_jogador
    assert "nome" in primeiro_jogador
    assert "idade" in primeiro_jogador
    assert "posicao" in primeiro_jogador
    assert "genero" in primeiro_jogador
    assert "nivel" in primeiro_jogador


def test_buscar_jogador_por_id_sucesso():
    id_valido = 1
    response = client.get(f"/jogadores/{id_valido}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data
    assert "nome" in data
    assert "idade" in data
    assert "posicao" in data
    assert "genero" in data
    assert "nivel" in data
    assert data["id"] == id_valido


def test_buscar_jogador_por_id_nao_encontrado():
    id_invalido = 999
    response = client.get(f"/jogadores/{id_invalido}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == f"Jogador com id {id_invalido} não encontrado."
