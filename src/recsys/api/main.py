from datetime import datetime
from fastapi import FastAPI, HTTPException

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.repositorio_interacao import RepositorioInteracaoMemoria
from recsys.strategies.recomendador_factory import RecomendadorFactory, TipoRecomendador

app = FastAPI(title="Sistema de Recomendação")

_repositorio = RepositorioInteracaoMemoria()
_usuarios: dict[str, Usuario] = {}
_catalogo: dict[str, Item] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/usuarios", status_code=201)
def criar_usuario(id: str, nome: str) -> Usuario:
    usuario = Usuario(id=id, nome=nome)
    _usuarios[usuario.id] = usuario
    return usuario


@app.post("/itens", status_code=201)
def criar_item(id: str, titulo: str, categoria: str) -> Item:
    item = Item(id=id, titulo=titulo, categoria=categoria)
    _catalogo[item.id] = item
    return item


@app.post("/interacoes", status_code=201)
def registrar_interacao(usuario_id: str, item_id: str, nota: float) -> dict[str, str]:
    if usuario_id not in _usuarios:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if item_id not in _catalogo:
        raise HTTPException(status_code=404, detail="Item nao encontrado")

    interacao = Interacao(
        usuario_id=usuario_id, item_id=item_id, nota=nota, timestamp=datetime.utcnow()
    )
    _repositorio.salvar(interacao)
    return {"status": "registrado"}


@app.get("/recomendacoes/{usuario_id}")
def recomendar(
    usuario_id: str, tipo: TipoRecomendador = TipoRecomendador.HIBRIDA, n: int = 5
) -> list[Item]:
    usuario = _usuarios.get(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    estrategia = RecomendadorFactory.criar(tipo, _repositorio, _catalogo)
    return estrategia.recomendar(usuario, n=n)
