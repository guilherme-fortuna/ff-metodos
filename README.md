# Gerenciador de Apostas

Aplicação FastAPI com SQLite para gerenciamento de depósitos e saques em casas de apostas, com dashboards por Dia/Semana/Mês/Ano.

## Requisitos
- Python 3.13 com venv (`python3.13-venv`)

## Instalação
```bash
cd /workspace
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar
```bash
./run.sh
# ou
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Funcionalidades
- Cadastro de Casas e Categorias
- Registro de Transações (depósito/saque) com data, valor e observação
- Dashboard com filtros por Dia, Semana, Mês, Ano e intervalo customizado

## Estrutura
- `app/main.py`: inicialização, rotas principais e seed de categorias
- `app/models.py`: modelos SQLModel (`Casa`, `Categoria`, `Transacao`)
- `app/routers/`: rotas de CRUD e dashboard
- `app/templates/`: templates Jinja2
- `app/static/`: estilos

## Observação
O banco SQLite é criado em `data.db` na raiz do projeto.