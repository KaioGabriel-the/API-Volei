import json
from typing import Dict
from pathlib import Path
from app.schemas.jogadores.jogador import JogadorCreate, Jogador


BASE_PATH = Path(__file__).resolve().parent / "data.json"


def read_database() -> dict:
    if not BASE_PATH.exists():
        return {"jogadores": []}
    with open(BASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    

def write_database(jogador : JogadorCreate) -> None:
    if BASE_PATH.exists():
        with open(BASE_PATH, "r", encoding="utf-8") as f:
            data: Dict = json.load(f)
    else:
        data = {"jogadores": []}

    next_id = max([j["id"] for j in data["jogadores"]], default=0) + 1
    jogador_com_id = Jogador(id=next_id, **jogador.model_dump(mode="json"))
    data["jogadores"].append(jogador_com_id.model_dump(mode="json"))
    
    with open(BASE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def delete_jogador(jogador_id: int) -> None:
    if not BASE_PATH.exists():
        raise ValueError("Banco de dados não encontrado")
    
    with open(BASE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    jogadores = data.get("jogadores", [])
    jogadores_atualizados = [j for j in jogadores if j["id"] != jogador_id]
    
    if len(jogadores) == len(jogadores_atualizados):
        raise ValueError("Jogador não encontrado")
    
    data["jogadores"] = jogadores_atualizados
    
    with open(BASE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)        
