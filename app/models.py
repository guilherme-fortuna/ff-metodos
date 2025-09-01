from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel


class Casa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=Column(String, unique=True, nullable=False, index=True))

    # relações omitidas; consultas farão joins explícitos


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=Column(String, unique=True, nullable=False, index=True))

    # relações omitidas; consultas farão joins explícitos


class Transacao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date = Field(default_factory=date.today)
    tipo: str = Field(description="deposito ou saque")
    valor: float = Field(description="Valor absoluto da transacao")
    observacao: Optional[str] = None

    casa_id: int = Field(foreign_key="casa.id")
    categoria_id: int = Field(foreign_key="categoria.id")

    # relações omitidas; consultas farão joins explícitos

