from typing import Any

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import commit, get_cursor
from .logic import calculate

router = APIRouter()

templates = Jinja2Templates(directory="client")


@router.get("/", response_class=HTMLResponse)
async def read_calculator(request: Request) -> Any:
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/calculate", response_class=JSONResponse)
async def calculate_expression(request: Request, expression: str) -> Any:
    get_cursor().execute("INSERT INTO request VALUES (?)", (expression,))
    commit()
    try:
        return {"result": calculate(expression)}
    except ValueError:
        return Response(content=f'"{expression}" is not a valid math expression', status_code=400)
    except NotImplementedError:
        return Response(content="calculation is not yet implemented", status_code=501)


@router.get("/history", response_class=JSONResponse)
async def read_history(request: Request) -> Any:
    result = get_cursor().execute("SELECT expression FROM request")
    return [row[0] for row in result.fetchall()]


app = FastAPI()
app.mount("/static", StaticFiles(directory="client"), name="static")
app.include_router(router)
