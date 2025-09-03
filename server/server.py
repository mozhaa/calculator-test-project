from typing import Any

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .logic import calculate

router = APIRouter()

templates = Jinja2Templates(directory="client")


@router.get("/")
async def read_calculator(request: Request) -> Any:
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/calculate")
async def calculate_expression(request: Request, expression: str) -> JSONResponse:
    try:
        return {"result": calculate(expression)}
    except ValueError:
        return Response(content=f'"{expression}" is not a valid math expression', return_code=400)
    except NotImplementedError:
        return Response(content="calculation is not yet implemented", return_code=501)


app = FastAPI()
app.mount("/static", StaticFiles(directory="client"), name="static")
app.include_router(router)
