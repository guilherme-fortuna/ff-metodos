from datetime import date, datetime

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlmodel import select
from sqlalchemy.orm import selectinload

from ..db import get_session
from ..models import Casa, Categoria, Transacao


router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))
templates.env.globals["now"] = datetime.now


@router.get("/", response_class=HTMLResponse)
def listar_transacoes(request: Request):
    with get_session() as session:
        stmt = select(Transacao).order_by(Transacao.data.desc(), Transacao.id.desc())
        transacoes = session.exec(stmt).all()
        casas = session.exec(select(Casa).order_by(Casa.nome)).all()
        categorias = session.exec(select(Categoria).order_by(Categoria.nome)).all()
    return templates.TemplateResponse(
        "transacoes.html",
        {"request": request, "transacoes": transacoes, "casas": casas, "categorias": categorias},
    )


@router.post("/criar")
def criar_transacao(
    data: date = Form(...),
    tipo: str = Form(...),
    valor: float = Form(...),
    casa_id: int = Form(...),
    categoria_id: int = Form(...),
    observacao: str = Form("")
):
    with get_session() as session:
        t = Transacao(
            data=data,
            tipo=tipo,
            valor=valor,
            casa_id=casa_id,
            categoria_id=categoria_id,
            observacao=observacao.strip() or None,
        )
        session.add(t)
        session.commit()
    return RedirectResponse(url="/transacoes/", status_code=303)


@router.post("/excluir/{transacao_id}")
def excluir_transacao(transacao_id: int):
    with get_session() as session:
        t = session.get(Transacao, transacao_id)
        if t:
            session.delete(t)
            session.commit()
    return RedirectResponse(url="/transacoes/", status_code=303)

