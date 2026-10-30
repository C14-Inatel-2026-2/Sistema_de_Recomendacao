from pydantic import BaseModel


class UsuarioIn(BaseModel):
    id: str
    nome: str


class ItemIn(BaseModel):
    id: str
    titulo: str
    categoria: str


class InteracaoIn(BaseModel):
    usuario_id: str
    item_id: str
    nota: float
