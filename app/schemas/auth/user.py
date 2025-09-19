from pydantic import BaseModel

class userCreate(BaseModel):
    username: str
    email: str
    password: str


