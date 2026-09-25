# DevShowcase API

API Backend para a atividade de Programação Backend.

## Tecnologias
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Como executar

1. Instale Python 3.11 ou superior.
2. Abra o terminal dentro desta pasta.
3. Crie um ambiente virtual:

```bash
python -m venv .venv
```

4. Ative:
- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows CMD: `.venv\Scripts\activate`

5. Instale as dependências:

```bash
pip install -r requirements.txt
```

6. Execute:

```bash
uvicorn app.main:app --reload
```

7. Abra no navegador:

`http://127.0.0.1:8000/docs`

A documentação interativa do FastAPI permitirá testar os endpoints.

## Endpoints exigidos

- POST /api/profiles
- GET /api/profiles/{id}
- POST /api/technologies
- GET /api/technologies
- POST /api/projects
- GET /api/projects

## Observação
O banco SQLite `devshowcase.db` é criado automaticamente na primeira execução.
