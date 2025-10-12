# tests/test_jogadores.py

from fastapi.testclient import TestClient
from main import app 
import pytest

from app.db.jogadores import DADOS_JOGADORES 

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_data():
    initial_data = DADOS_JOGADORES.copy() 
    
    yield 
    DADOS_JOGADORES.clear()
    DADOS_JOGADORES.extend(initial_data)


def test_criar_jogador_sucesso():
    novo_jogador_data = {
        "nome": "Leila Barros",
        "idade": 49,
        "genero": "FEMININO",
        "posicao": "OPOSTO",
        "nivel": "EXPERIENTE"
    }
    
    response = client.post("/jogadores/", json=novo_jogador_data)
    
    assert response.status_code == 201
    
    data = response.json()
    
    assert "id" in data
    
    assert isinstance(data["id"], int)
    

def test_criar_jogador_falha_validacao_campos_ausentes():
    dados_invalidos = {
        "nome": "Zeca",
        "idade": 25,
    }
    
    response = client.post("/jogadores/", json=dados_invalidos)
    
    assert response.status_code == 422
    
    data = response.json()
    
    assert "detail" in data
    
    erro_genero = next((err for err in data["detail"] if err["loc"] == ["body", "genero"]), None)
    assert erro_genero is not None
    assert "Field required" in erro_genero["msg"] or "field required" in erro_genero["msg"] 
    