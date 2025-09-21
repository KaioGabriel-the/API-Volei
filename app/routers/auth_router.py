from fastapi import APIRouter
from app.schemas.auth.user import userCreate

router = APIRouter()

@router.post("/registro", response_model=userCreate)
async def register_user(user: userCreate):
    return user
    


@router.post("/login")
async def login_user():
    return "Usuário logado com sucesso"