import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.repositorio_interacao import RepositorioInteracaoMemoria
from recsys.strategies.recomendador_factory import RecomendadorFactory, TipoRecomendador

app = FastAPI(title="Sistema de Recomendação")

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

_repositorio = RepositorioInteracaoMemoria()
_usuarios: dict[str, Usuario] = {}
_catalogo: dict[str, Item] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/usuarios", response_model=Usuario)
def criar_usuario(id: str, nome: str) -> Usuario:
    usuario = Usuario(id=id, nome=nome)
    _usuarios[usuario.id] = usuario
    return usuario

@app.get("/usuarios", response_model=list[Usuario])
def listar_usuarios() -> list[Usuario]:
    return list(_usuarios.values())


@app.post("/itens", response_model=Item)
def criar_item(id: str, titulo: str, categoria: str) -> Item:
    item = Item(id=id, titulo=titulo, categoria=categoria)
    _catalogo[item.id] = item
    return item

@app.get("/itens", response_model=list[Item])
def listar_itens() -> list[Item]:
    return list(_catalogo.values())

@app.post("/interacoes", status_code=201)
def registrar_interacao(usuario_id: str, item_id: str, nota: float) -> dict[str, str]:
    if usuario_id not in _usuarios:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if item_id not in _catalogo:
        raise HTTPException(status_code=404, detail="Item nao encontrado")

    interacao = Interacao(
        usuario_id=usuario_id, item_id=item_id, nota=nota, timestamp=datetime.now(timezone.utc)
    )
    _repositorio.salvar(interacao)
    return {"status": "registrado"}


@app.get("/recomendacoes/{usuario_id}", response_model=list[Item])
def recomendar(
    usuario_id: str, tipo: TipoRecomendador = TipoRecomendador.HIBRIDA, n: int = 5
) -> list[Item]:
    usuario = _usuarios.get(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    estrategia = RecomendadorFactory.criar(tipo, _repositorio, _catalogo)
    return estrategia.recomendar(usuario, n=n)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
