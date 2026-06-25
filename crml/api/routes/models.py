from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ModelInfo(BaseModel):
    name: str
    version: str
    task: str


@router.get("/models", response_model=list[ModelInfo])
async def list_models():
    # Step 5 (model registry) will return real model data here
    raise HTTPException(status_code=501, detail="Model registry not yet implemented")
