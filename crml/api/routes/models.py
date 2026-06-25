from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class ModelInfo(BaseModel):
    name: str
    version: str
    task: str
    created_at: str


@router.get("/models", response_model=list[ModelInfo])
async def list_models(request: Request):
    registry = request.app.state.registry
    return [ModelInfo(**e.to_dict()) for e in registry.list()]
