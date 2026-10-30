import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

from recsys.api.schemas import InteracaoIn, ItemIn, UsuarioIn
from recsys.domain.interacao import Interacao, ultimas_interacoes
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.excecoes import EntidadeJaExiste
from recsys.repositories.repositorios import Repositorios, criar_repositorios_sqlite
from recsys.seed import popular_se_vazio
from recsys.strategies.recomendador_factory import RecomendadorFactory, TipoRecomendador

router = APIRouter()


def obter_repositorios(request: Request) -> Repositorios:
    return request.app.state.repositorios


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/usuarios", response_model=Usuario, status_code=201)
def criar_usuario(dados: UsuarioIn, repos: Repositorios = Depends(obter_repositorios)) -> Usuario:
    try:
        usuario = Usuario(id=dados.id, nome=dados.nome)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    try:
        repos.usuarios.salvar(usuario)
    except EntidadeJaExiste as e:
        raise HTTPException(status_code=409, detail="Usuário já existe") from e
    return usuario


@router.get("/usuarios", response_model=list[Usuario])
def listar_usuarios(repos: Repositorios = Depends(obter_repositorios)) -> list[Usuario]:
    return repos.usuarios.listar()


@router.get("/usuarios/{usuario_id}/avaliacoes", response_model=dict[str, float])
def listar_avaliacoes(
    usuario_id: str, repos: Repositorios = Depends(obter_repositorios)
) -> dict[str, float]:
    """Nota vigente (a mais recente) que o usuário deu a cada item: {item_id: nota}."""
    if repos.usuarios.buscar_por_id(usuario_id) is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    vigentes = ultimas_interacoes(repos.interacoes.buscar_por_usuario(usuario_id))
    return {i.item_id: i.nota for i in vigentes}


@router.post("/itens", response_model=Item, status_code=201)
def criar_item(dados: ItemIn, repos: Repositorios = Depends(obter_repositorios)) -> Item:
    try:
        item = Item(id=dados.id, titulo=dados.titulo, categoria=dados.categoria)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    try:
        repos.itens.salvar(item)
    except EntidadeJaExiste as e:
        raise HTTPException(status_code=409, detail="Item já existe") from e
    return item


@router.get("/itens", response_model=list[Item])
def listar_itens(repos: Repositorios = Depends(obter_repositorios)) -> list[Item]:
    return repos.itens.listar()


@router.post("/interacoes", status_code=201)
def registrar_interacao(
    dados: InteracaoIn, repos: Repositorios = Depends(obter_repositorios)
) -> dict[str, str]:
    if repos.usuarios.buscar_por_id(dados.usuario_id) is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if repos.itens.buscar_por_id(dados.item_id) is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    try:
        interacao = Interacao(
            usuario_id=dados.usuario_id,
            item_id=dados.item_id,
            nota=dados.nota,
            timestamp=datetime.now(timezone.utc),
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    repos.interacoes.salvar(interacao)
    return {"status": "registrado"}


@router.get("/recomendacoes/{usuario_id}", response_model=list[Item])
def recomendar(
    usuario_id: str,
    tipo: TipoRecomendador = TipoRecomendador.HIBRIDA,
    n: int = Query(5, ge=1, le=50),
    repos: Repositorios = Depends(obter_repositorios),
) -> list[Item]:
    usuario = repos.usuarios.buscar_por_id(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    catalogo = {item.id: item for item in repos.itens.listar()}
    estrategia = RecomendadorFactory.criar(tipo, repos.interacoes, catalogo)
    return estrategia.recomendar(usuario, n=n)


def criar_app(repositorios: Repositorios | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        dono_dos_repositorios = app.state.repositorios is None
        if dono_dos_repositorios:
            app.state.repositorios = criar_repositorios_sqlite(
                os.getenv("DATABASE_PATH", "recsys.db")
            )
            popular_se_vazio(app.state.repositorios)
        yield
        if dono_dos_repositorios:
            app.state.repositorios.fechar()

    app = FastAPI(title="Sistema de Recomendação", lifespan=lifespan)
    app.state.repositorios = repositorios

    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app
