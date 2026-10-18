from datetime import datetime, timezone

import uvicorn
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.repositorio_interacao import RepositorioInteracaoMemoria
from recsys.seed import popular
from recsys.strategies.recomendador_factory import RecomendadorFactory, TipoRecomendador

app = FastAPI(title="Sistema de Recomendação")

origins = os.getenv(
    "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

_repositorio = RepositorioInteracaoMemoria()
_usuarios: dict[str, Usuario] = {}
_catalogo: dict[str, Item] = {}

popular(_usuarios, _catalogo, _repositorio)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/usuarios", response_model=Usuario, status_code=201)
def criar_usuario(dados: UsuarioIn) -> Usuario:
    if dados.id in _usuarios:
        raise HTTPException(status_code=409, detail="Usuário já existe")
    try:
        usuario = Usuario(id=dados.id, nome=dados.nome)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    _usuarios[usuario.id] = usuario
    return usuario

@app.get("/usuarios", response_model=list[Usuario])
def listar_usuarios() -> list[Usuario]:
    return list(_usuarios.values())

@app.get("/usuarios/{usuario_id}/avaliacoes", response_model=dict[str, float])
def listar_avaliacoes(usuario_id: str) -> dict[str, float]:
    """Nota mais recente que o usuário deu a cada item: {item_id: nota}."""
    if usuario_id not in _usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {i.item_id: i.nota for i in _repositorio.buscar_por_usuario(usuario_id)}

@app.post("/itens", response_model=Item, status_code=201)
def criar_item(dados: ItemIn) -> Item:
    if dados.id in _catalogo:
        raise HTTPException(status_code=409, detail="Item já existe")
    try:
        item = Item(id=dados.id, titulo=dados.titulo, categoria=dados.categoria)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    _catalogo[item.id] = item
    return item

@app.get("/itens", response_model=list[Item])
def listar_itens() -> list[Item]:
    return list(_catalogo.values())

@app.post("/interacoes", status_code=201)
def registrar_interacao(dados: InteracaoIn) -> dict[str, str]:
    if dados.usuario_id not in _usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if dados.item_id not in _catalogo:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    try:
        interacao = Interacao(
            usuario_id=dados.usuario_id,
            item_id=dados.item_id,
            nota=dados.nota,
            timestamp=datetime.now(timezone.utc),
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    _repositorio.salvar(interacao)
    return {"status": "registrado"}

@app.get("/recomendacoes/{usuario_id}", response_model=list[Item])
def recomendar(
    usuario_id: str, tipo: TipoRecomendador = TipoRecomendador.HIBRIDA, n: int = 5
) -> list[Item]:
    usuario = _usuarios.get(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    estrategia = RecomendadorFactory.criar(tipo, _repositorio, _catalogo)
    return estrategia.recomendar(usuario, n=n)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
