from fastapi.testclient import TestClient
from main import app 
from app.db.jogadores import DADOS_JOGADORES 
import pytest 

@pytest.fixture(autouse=True)
def cleanup_data():
    initial_data = DADOS_JOGADORES.copy() 
    
    yield 
    DADOS_JOGADORES.clear()
    DADOS_JOGADORES.extend(initial_data)


client = TestClient(app)


def test_deletar_jogador_sucesso():
    id_a_deletar = 1 
    
    tamanho_antes = len(DADOS_JOGADORES)
    
    response = client.delete(f"/jogadores/{id_a_deletar}")
    
    assert response.status_code == 204
    
    assert response.text == ""
    
    assert len(DADOS_JOGADORES) == tamanho_antes - 1
    
    jogador_removido = next((item for item in DADOS_JOGADORES if item["id"] == id_a_deletar), None)
    assert jogador_removido is None


def test_deletar_jogador_nao_encontrado():
    id_inexistente = 999 
    
    tamanho_antes = len(DADOS_JOGADORES)
    
    response = client.delete(f"/jogadores/{id_inexistente}")
    
    assert response.status_code == 404
    
    data = response.json()
    
    assert "detail" in data
    assert data["detail"] == f"Jogador com id {id_inexistente} não encontrado para exclusão."
    
    assert len(DADOS_JOGADORES) == tamanho_antes
