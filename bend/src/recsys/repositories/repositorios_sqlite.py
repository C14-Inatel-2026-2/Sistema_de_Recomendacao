"""Implementações SQLite dos repositórios (apenas biblioteca padrão)."""
import json
import sqlite3
import threading
from collections.abc import Sequence
from datetime import datetime
from typing import Any

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.excecoes import EntidadeJaExiste
from recsys.repositories.repositorio_interacao import RepositorioInteracao
from recsys.repositories.repositorio_item import RepositorioItem
from recsys.repositories.repositorio_usuario import RepositorioUsuario

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id           TEXT PRIMARY KEY,
    nome         TEXT NOT NULL,
    preferencias TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS itens (
    id        TEXT PRIMARY KEY,
    titulo    TEXT NOT NULL,
    categoria TEXT NOT NULL,
    atributos TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS interacoes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id TEXT NOT NULL REFERENCES usuarios(id),
    item_id    TEXT NOT NULL REFERENCES itens(id),
    nota       REAL NOT NULL CHECK (nota BETWEEN 0 AND 5),
    timestamp  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_interacoes_usuario ON interacoes(usuario_id);
"""


class ConexaoSQLite:
    """Uma conexão compartilhada e protegida por lock.

    O FastAPI executa endpoints síncronos em um pool de threads, então a
    conexão precisa aceitar uso multithread. Compartilhar uma única conexão
    também faz o ":memory:" funcionar (cada conexão teria seu próprio banco).
    """

    def __init__(self, caminho: str = ":memory:") -> None:
        self._conn = sqlite3.connect(caminho, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._lock = threading.RLock()
        with self._lock:
            self._conn.executescript(_ESQUEMA)

    def executar(self, sql: str, params: Sequence[Any] = ()) -> None:
        with self._lock, self._conn:
            self._conn.execute(sql, params)

    def consultar(self, sql: str, params: Sequence[Any] = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self._conn.execute(sql, params).fetchall()

    def fechar(self) -> None:
        with self._lock:
            self._conn.close()


class RepositorioUsuarioSQLite(RepositorioUsuario):
    def __init__(self, conexao: ConexaoSQLite) -> None:
        self._conexao = conexao

    def salvar(self, usuario: Usuario) -> None:
        try:
            self._conexao.executar(
                "INSERT INTO usuarios (id, nome, preferencias) VALUES (?, ?, ?)",
                (usuario.id, usuario.nome, json.dumps(usuario.preferencias)),
            )
        except sqlite3.IntegrityError as erro:
            raise EntidadeJaExiste("Usuário", usuario.id) from erro

    def buscar_por_id(self, usuario_id: str) -> Usuario | None:
        linhas = self._conexao.consultar("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
        return self._para_usuario(linhas[0]) if linhas else None

    def listar(self) -> list[Usuario]:
        linhas = self._conexao.consultar("SELECT * FROM usuarios ORDER BY rowid")
        return [self._para_usuario(linha) for linha in linhas]

    @staticmethod
    def _para_usuario(linha: sqlite3.Row) -> Usuario:
        return Usuario(
            id=linha["id"], nome=linha["nome"], preferencias=json.loads(linha["preferencias"])
        )


class RepositorioItemSQLite(RepositorioItem):
    def __init__(self, conexao: ConexaoSQLite) -> None:
        self._conexao = conexao

    def salvar(self, item: Item) -> None:
        try:
            self._conexao.executar(
                "INSERT INTO itens (id, titulo, categoria, atributos) VALUES (?, ?, ?, ?)",
                (item.id, item.titulo, item.categoria, json.dumps(item.atributos)),
            )
        except sqlite3.IntegrityError as erro:
            raise EntidadeJaExiste("Item", item.id) from erro

    def buscar_por_id(self, item_id: str) -> Item | None:
        linhas = self._conexao.consultar("SELECT * FROM itens WHERE id = ?", (item_id,))
        return self._para_item(linhas[0]) if linhas else None

    def listar(self) -> list[Item]:
        linhas = self._conexao.consultar("SELECT * FROM itens ORDER BY rowid")
        return [self._para_item(linha) for linha in linhas]

    @staticmethod
    def _para_item(linha: sqlite3.Row) -> Item:
        return Item(
            id=linha["id"],
            titulo=linha["titulo"],
            categoria=linha["categoria"],
            atributos=json.loads(linha["atributos"]),
        )


class RepositorioInteracaoSQLite(RepositorioInteracao):
    def __init__(self, conexao: ConexaoSQLite) -> None:
        self._conexao = conexao

    def salvar(self, interacao: Interacao) -> None:
        self._conexao.executar(
            "INSERT INTO interacoes (usuario_id, item_id, nota, timestamp) VALUES (?, ?, ?, ?)",
            (interacao.usuario_id, interacao.item_id, interacao.nota, interacao.timestamp.isoformat()),
        )

    def buscar_por_usuario(self, usuario_id: str) -> list[Interacao]:
        linhas = self._conexao.consultar(
            "SELECT * FROM interacoes WHERE usuario_id = ? ORDER BY id", (usuario_id,)
        )
        return [self._para_interacao(linha) for linha in linhas]

    def buscar_todas(self) -> list[Interacao]:
        linhas = self._conexao.consultar("SELECT * FROM interacoes ORDER BY id")
        return [self._para_interacao(linha) for linha in linhas]

    @staticmethod
    def _para_interacao(linha: sqlite3.Row) -> Interacao:
        return Interacao(
            usuario_id=linha["usuario_id"],
            item_id=linha["item_id"],
            nota=linha["nota"],
            timestamp=datetime.fromisoformat(linha["timestamp"]),
        )
