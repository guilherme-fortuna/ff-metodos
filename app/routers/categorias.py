from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from ..db import get_session
from ..models import Categoria


router = APIRouter()
templates = Jinja2Templates(directory=str(__file__).rsplit("routers", 1)[0] + "templates")


@router.get("/", response_class=HTMLResponse)
def listar_categorias(request: Request):
    with get_session() as session:
        categorias = session.exec(select(Categoria).order_by(Categoria.nome)).all()
    return templates.TemplateResponse("categorias.html", {"request": request, "categorias": categorias})


@router.post("/criar")
def criar_categoria(nome: str = Form(...)):
    with get_session() as session:
        categoria = Categoria(nome=nome.strip())
        session.add(categoria)
        session.commit()
    return RedirectResponse(url="/categorias/", status_code=303)


@router.post("/excluir/{categoria_id}")
def excluir_categoria(categoria_id: int):
    with get_session() as session:
        categoria = session.get(Categoria, categoria_id)
        if categoria:
            session.delete(categoria)
            session.commit()
    return RedirectResponse(url="/categorias/", status_code=303)


@router.post("/editar/{categoria_id}")
def editar_categoria(categoria_id: int, nome: str = Form(...)):
    with get_session() as session:
        categoria = session.get(Categoria, categoria_id)
        if categoria:
            categoria.nome = nome.strip()
            session.add(categoria)
            session.commit()
    return RedirectResponse(url="/categorias/", status_code=303)

