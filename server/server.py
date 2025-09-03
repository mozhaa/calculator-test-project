from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import FileResponse, JSONResponse

from .logic import calculate

router = APIRouter()


@router.get("/")
async def read_calculator(request: Request) -> FileResponse:
    return FileResponse("client/index.html")


@router.post("/calculate")
async def calculate_expression(request: Request, expression: str) -> JSONResponse:
    try:
        return {"result": calculate(expression)}
    except ValueError:
        return Response(content=f'"{expression}" is not a valid math expression', return_code=400)
    except NotImplementedError:
        return Response(content="calculation is not yet implemented", return_code=501)


app = FastAPI()
app.include_router(router)
