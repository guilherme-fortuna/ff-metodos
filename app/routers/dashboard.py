from datetime import date, datetime, timedelta
from typing import Dict, Tuple

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from ..db import get_session
from ..models import Categoria, Transacao


router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))
templates.env.globals["now"] = datetime.now


def _compute_range(range_key: str, start: date | None, end: date | None) -> Tuple[date, date]:
    today = date.today()
    if range_key == "dia":
        return today, today
    if range_key == "semana":
        start_day = today - timedelta(days=today.weekday())
        end_day = start_day + timedelta(days=6)
        return start_day, end_day
    if range_key == "mes":
        first = today.replace(day=1)
        if first.month == 12:
            next_first = first.replace(year=first.year + 1, month=1)
        else:
            next_first = first.replace(month=first.month + 1)
        last = next_first - timedelta(days=1)
        return first, last
    if range_key == "ano":
        first = date(today.year, 1, 1)
        last = date(today.year, 12, 31)
        return first, last
    # custom
    if not start or not end:
        return today, today
    return start, end


@router.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    faixa: str = Query("mes", description="dia|semana|mes|ano|custom"),
    inicio: date | None = Query(None),
    fim: date | None = Query(None),
):
    start, end = _compute_range(faixa, inicio, fim)
    with get_session() as session:
        stmt = select(Transacao).where(Transacao.data >= start, Transacao.data <= end)
        transacoes = session.exec(stmt).all()

    total_depositos = sum(t.valor for t in transacoes if t.tipo == "deposito")
    total_saques = sum(t.valor for t in transacoes if t.tipo == "saque")
    saldo = total_saques - total_depositos

    por_categoria: Dict[str, float] = {}
    with get_session() as session:
        categorias = {c.id: c.nome for c in session.exec(select(Categoria)).all()}
    for t in transacoes:
        nome = categorias.get(t.categoria_id, "Sem categoria")
        por_categoria[nome] = por_categoria.get(nome, 0.0) + (t.valor if t.tipo == "saque" else -t.valor)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "start": start,
            "end": end,
            "faixa": faixa,
            "total_depositos": total_depositos,
            "total_saques": total_saques,
            "saldo": saldo,
            "por_categoria": por_categoria,
        },
    )

