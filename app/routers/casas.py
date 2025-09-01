from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlmodel import Session, select

from ..db import get_session
from ..models import Casa


router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
def listar_casas(request: Request):
    with get_session() as session:
        casas = session.exec(select(Casa).order_by(Casa.nome)).all()
    return templates.TemplateResponse("casas.html", {"request": request, "casas": casas})


@router.post("/criar")
def criar_casa(nome: str = Form(...), link: str = Form("") ):
    with get_session() as session:
        casa = Casa(nome=nome.strip(), link=(link.strip() or None))
        session.add(casa)
        session.commit()
    return RedirectResponse(url="/casas/", status_code=303)


@router.post("/excluir/{casa_id}")
def excluir_casa(casa_id: int):
    with get_session() as session:
        casa = session.get(Casa, casa_id)
        if casa:
            session.delete(casa)
            session.commit()
    return RedirectResponse(url="/casas/", status_code=303)


@router.post("/editar/{casa_id}")
def editar_casa(casa_id: int, nome: str = Form(...), link: str = Form("")):
    with get_session() as session:
        casa = session.get(Casa, casa_id)
        if casa:
            casa.nome = nome.strip()
            casa.link = link.strip() or None
            session.add(casa)
            session.commit()
    return RedirectResponse(url="/casas/", status_code=303)

