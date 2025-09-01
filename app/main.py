from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .db import create_db_and_tables, get_session
from .models import Transacao
from .routers.dashboard import router as dashboard_router
from .routers.casas import router as casas_router
from .routers.categorias import router as categorias_router
from .routers.transacoes import router as transacoes_router
from sqlmodel import Session, select


BASE_DIR = Path(__file__).resolve().parent
templates_dir = BASE_DIR / "templates"

app = FastAPI(title="Gerenciador de Apostas")

templates = Jinja2Templates(directory=str(templates_dir))
templates.env.globals["now"] = datetime.now


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()
    # Seed categorias padrao
    from .models import Categoria
    with get_session() as session:
        existentes = {c.nome for c in session.exec(select(Categoria)).all()}
        padroes = [
            "Giros grátis",
            "Promoção",
            "Com risco",
            "Sem risco",
        ]
        for nome in padroes:
            if nome not in existentes:
                session.add(Categoria(nome=nome))
        session.commit()


app.include_router(dashboard_router)
app.include_router(casas_router, prefix="/casas", tags=["Casas"])
app.include_router(categorias_router, prefix="/categorias", tags=["Categorias"])
app.include_router(transacoes_router, prefix="/transacoes", tags=["Transações"])


@app.get("/health", response_class=HTMLResponse)
def health(_: Request) -> str:
    return "OK"

